import datetime
import os
import socket
import threading
import time

from common.setup_logger import setup_logger
from common.setup_selenium import setup_selenium
from constants.logs_location import LogsLocation
from constants.webdriver_type import WebDriverType
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()
CHATGPT_EMAIL_ADDRESS = os.getenv("CHATGPT_EMAIL_ADDRESS")
CHATGPT_PASSWORD = os.getenv("CHATGPT_PASSWORD")


class AutoChatGPT:
    OPENAI_URL = "https://chat.openai.com"

    def __init__(
        self, chrome_path, logs_location=LogsLocation.GENERATOR.value
    ):
        self.port = self.__find_available_port()
        self.logger = setup_logger(__name__, logs_location)
        self.chrome_path = chrome_path
        self.__setup(self.port, AutoChatGPT.OPENAI_URL)
        self.check_login_status()

    def __find_available_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def __setup(self, port, url):
        self.__launch_chrome_with_remote_debugging(port, url)
        self.driver = self.__setup_webdriver(self.port)

    def __launch_chrome_with_remote_debugging(self, port, url):
        def open_chrome():
            chrome_cmd = (
                f"{self.chrome_path} --remote-debugging-port={port} {url}"
            )
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()
        time.sleep(5)
        self.logger.debug("New Chrome window has been opened")

    def __setup_webdriver(self, port):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{port}"
        )
        driver = setup_selenium(WebDriverType.CHROME_DRIVER, chrome_options)
        return driver

    def __login_openai(self, email_address, password):
        wait = WebDriverWait(self.driver, 10)

        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@class, 'btn-neutral') and .//div[contains(text(), 'Log in')]]",
                )
            )
        ).click()

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[name="email"]')
            )
        ).send_keys(email_address)

        self.driver.find_element(
            By.CSS_SELECTOR, "button.continue-btn"
        ).click()

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[name="password"]')
            )
        ).send_keys(password)

        self.driver.find_element(
            By.CSS_SELECTOR, 'button[data-action-button-primary="true"]'
        ).click()

    def quit(self):
        self.logger.debug("Closing the browser")
        self.driver.close()
        self.driver.quit()

    def restart(self, port, url):
        self.quit()
        time.sleep(5)
        self.__setup(port, url)
        time.sleep(5)

    def auto_login(
        self, email_address=CHATGPT_EMAIL_ADDRESS, password=CHATGPT_PASSWORD
    ):
        self.logger.debug("Login to ChatGPT")
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                self.__login_openai(email_address, password)
                break
            except TimeoutException:
                self.logger.warning(
                    f"Login issue occurred. Retrying {retry_count + 1}/{max_retries}"
                )
                self.restart(self.port, AutoChatGPT.OPENAI_URL)
                retry_count += 1

        if retry_count == max_retries:
            self.logger.error("Login failed, end working session")
            self.quit()
            return
        time.sleep(5)
        self.logger.debug("Login successfully")

    def new_conversation(self):
        try:
            self.driver.find_element(By.LINK_TEXT, "New chat").click()
        except ElementClickInterceptedException:
            pass

    def __save_conversation(self, response, file_name):
        directory_name = "conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        response = response.replace('"', "")
        with open(
            os.path.join(directory_name, file_name), "a", encoding="utf-8"
        ) as file:
            file.write(f"{response}\n")

    def set_chatgpt_version(self, model_version):
        if model_version not in ["GPT-3.5", "GPT-4"]:
            msg = "model_version must be GPT-3.5 or GPT-4"
            raise ValueError(msg)
        self.driver.find_element(
            By.XPATH, f"//button[contains(., '{model_version}')]"
        ).click()

    def check_login_status(self):
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button[contains(@class, 'btn-neutral') and .//div[contains(text(), 'Log in')]]",
                    )
                )
            )
            self.auto_login()
        except TimeoutException:
            try:
                wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//textarea[contains(@id, 'prompt-textarea')]",
                        )
                    )
                )
            except TimeoutException:
                self.restart(self.port, AutoChatGPT.OPENAI_URL)
                self.auto_login()

    def send_prompt_to_chatgpt(self, prompt):
        self.logger.debug(
            'Sending prompt has content: "' + prompt + '" to ChatGPT'
        )
        wait = WebDriverWait(self.driver, 10)
        input_box = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[contains(@id, 'prompt-textarea')]")
            )
        )
        self.driver.execute_script(
            f"arguments[0].value = '{prompt}';", input_box
        )
        input_box.send_keys(Keys.RETURN)
        input_box.submit()
        self.logger.debug("Prompt has been sent. Waiting for response.")

    def get_chatgpt_response(self, max_retries=4):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "result-streaming")]')
            ),
        )

        WebDriverWait(self.driver, 60).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "result-streaming")]')
            ),
        )

        gpt_elements = self.driver.find_elements(
            By.XPATH,
            '//div[contains(@class, "markdown")]',
        )
        self.logger.debug("Generated sucessfully")

        retry_count = 0
        while retry_count < max_retries:
            try:
                response = gpt_elements[-1].text
                return response
            except Exception:
                self.logger.debug(
                    f"Failed to get response. Retrying {retry_count + 1}/{max_retries}"
                )
                self.driver.refresh()
                time.sleep(5)
                retry_count += 1
            if retry_count == max_retries:
                self.logger.debug(
                    f"Failed to get response after {max_retries} retries."
                )
        return ""

    def generate_for_predefined_prompts(self, prompts, max_retries=4):
        kickoff_time = str(datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        file_name = "response_" + kickoff_time + ".txt"

        for prompt in prompts:
            prompt_content, prompt_repeat_time = prompt[0], prompt[1]
            for turn in range(prompt_repeat_time):
                if turn % 2 == 0 and turn != 0:
                    self.new_conversation()
                    time.sleep(3)
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        self.send_prompt_to_chatgpt(prompt_content)
                        response = self.get_chatgpt_response()
                        break
                    except TimeoutException:
                        self.logger.warning(
                            f"Timeout occurred for prompt: '{prompt_content}'. Retrying {retry_count + 1}/{max_retries}"
                        )
                        self.driver.refresh()
                        time.sleep(5)
                        retry_count += 1
                if retry_count == max_retries:
                    self.logger.error(
                        f"Failed to get response for prompt: '{prompt_content}' after {max_retries} retries."
                    )
                    self.quit()
                    return
                self.__save_conversation(response, file_name)
        self.quit()
