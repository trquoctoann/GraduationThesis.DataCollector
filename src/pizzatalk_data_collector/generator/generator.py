import datetime
import os
import threading
import time

from common.setup_logger import setup_logger
from common.setup_selenium import setup_selenium
from constants.logs_location import LogsLocation
from constants.webdriver_type import WebDriverType
from dotenv import load_dotenv
from generator.login import bypassing_cloudflare, login_openai
from generator.utils import find_available_port
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()
CHATGPT_EMAIL_ADDRESS = os.getenv("CHATGPT_EMAIL_ADDRESS")
CHATGPT_PASSWORD = os.getenv("CHATGPT_PASSWORD")

prompts = [
    [
        "giả sử bạn là khách hàng muốn đặt bánh pizza online, tạo 20 câu nhắn tin với shop để đặt bánh. Mẫu câu cần phù hợp với mô hình nhận diện thực thể.",
        1,
    ],
    ["tiếp tục tạo 20 câu, không trùng với các câu trước đó", 9],
]


class ChatGPTGenerator:
    OPENAI_URL = "https://chat.openai.com/"

    def __init__(self, chrome_path):
        self.port = find_available_port()
        self.logger = setup_logger(__name__, LogsLocation.GENERATOR.value)
        self.chrome_path = chrome_path
        self.is_login = False
        self.__setup()

    def __setup(self):
        self.__launch_chrome_with_remote_debugging(
            self.port, ChatGPTGenerator.OPENAI_URL
        )
        self.driver = self.__setup_webdriver(self.port)

    def __launch_chrome_with_remote_debugging(self, port, url):
        def open_chrome():
            chrome_cmd = f"{self.chrome_path} --incognito --remote-debugging-port={port} {url}"
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()
        time.sleep(5)
        self.logger.debug(
            "New Chrome window in Incognito mode has been opened"
        )

    def __setup_webdriver(self, port):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{port}"
        )
        driver = setup_selenium(WebDriverType.CHROME_DRIVER, chrome_options)
        return driver

    def quit(self):
        self.logger.debug("Closing the browser")
        self.driver.close()
        self.driver.quit()

    def restart(self):
        self.quit()
        time.sleep(5)
        self.__setup()
        time.sleep(5)

    def auto_login(
        self, email_address=CHATGPT_EMAIL_ADDRESS, password=CHATGPT_PASSWORD
    ):
        self.logger.debug("Login to ChatGPT")
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                login_openai(self.driver, email_address, password)
                self.is_login = True
                break
            except TimeoutException:
                self.logger.warning(
                    f"Login issue occurred. Retrying {retry_count + 1}/{max_retries}"
                )
                self.restart()
                retry_count += 1

        if retry_count == max_retries:
            self.logger.error("Login failed, end working session")
            self.quit()
            return
        time.sleep(5)
        self.logger.debug("Login successfully")

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
        if not self.is_login:
            self.logger.error("Unauthorized request")
            return False
        return True

    def send_prompt_to_chatgpt(self, prompt):
        if not self.check_login_status():
            return
        self.logger.debug(
            'Sending prompt has content: "'
            + prompt
            + '" to ChatGPT. Waiting for response'
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

    def get_chatgpt_response(self):
        if not self.check_login_status():
            return

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
        return gpt_elements[-1].text

    def generate_for_predefined_prompts(self, prompts=prompts, max_retries=3):
        if not self.check_login_status():
            return
        kickoff_time = str(datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        file_name = "response_" + kickoff_time + ".txt"

        for prompt in prompts:
            prompt_content, prompt_repeat_time = prompt[0], prompt[1]
            for turn in range(prompt_repeat_time):
                retry_count = 0
                while retry_count < max_retries:
                    self.send_prompt_to_chatgpt(prompt_content)
                    try:
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
                    continue
                self.__save_conversation(response, file_name)
        self.quit()
