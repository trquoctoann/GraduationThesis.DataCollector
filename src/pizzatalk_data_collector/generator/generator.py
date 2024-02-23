import os
import time
from datetime import datetime, timedelta

from common.auto_chatgpt import AutoChatGPT
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from generator.aggregate_generator_result import (
    aggregate_specified_date_response,
)
from selenium.common.exceptions import TimeoutException

prompts = [
    [
        "Suppose you are a customer order pizza online and you just completed your order. Create 15 text messages to the shop to provide your information for shipping process. The sentence format should be compatible with the entity recognition model.",
        10,
    ]
]


class Generator:
    def __init__(self):
        self.logger = setup_logger(__name__, LogsLocation.GENERATOR.value)
        self.chatgpt = AutoChatGPT()

    def __save_response(self, response, file_name):
        self.logger.debug(f"Saving response to {file_name}")
        directory_name = "conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        response = response.replace('"', "")
        with open(
            os.path.join(directory_name, file_name), "a", encoding="utf-8"
        ) as file:
            file.write(f"{response}\n")
        self.logger.debug(f"Response saved at {str(datetime.now())}")

    def __generate_for_predefined_prompts(self, prompts, max_retries=4):
        kickoff_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
        file_name = "response_" + kickoff_time + ".txt"

        for prompt in prompts:
            prompt_content, prompt_repeat_time = prompt[0], prompt[1]
            for turn in range(prompt_repeat_time):
                if turn % 2 == 0 and turn != 0:
                    self.chatgpt.new_conversation()
                    time.sleep(3)
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        self.chatgpt.send_prompt_to_chatgpt(prompt_content)
                        response = self.chatgpt.get_chatgpt_response()
                        break
                    except TimeoutException:
                        self.chatgpt.logger.warning(
                            f"Timeout occurred for prompt: '{prompt_content}'. Retrying {retry_count + 1}/{max_retries}"
                        )
                        self.chatgpt.driver.refresh()
                        time.sleep(5)
                        retry_count += 1
                if retry_count == max_retries:
                    self.chatgpt.logger.error(
                        f"Failed to get response for prompt: '{prompt_content}' after {max_retries} retries."
                    )
                    self.chatgpt.quit()
                    return
                self.__save_response(response, file_name)
        self.chatgpt.quit()

    def start_generate(self, prompts=prompts):
        self.logger.debug("Start using ChatGPT to generate data")
        today = datetime.now()
        if today.hour == 0 and today.minute == 0:
            yesterday = datetime.now() - timedelta(days=1)
            aggregate_specified_date_response(yesterday.strftime("%Y%m%d"))

        self.__generate_for_predefined_prompts(prompts)
        self.logger.debug("Complete generating")
