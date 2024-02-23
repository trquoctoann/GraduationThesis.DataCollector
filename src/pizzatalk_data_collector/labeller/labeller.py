import json
import os
import time
from datetime import datetime

from common.auto_chatgpt import AutoChatGPT
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from labeller.utils import read_lines_from_given_position
from selenium.common.exceptions import TimeoutException


class Labeller:
    BASE_PROMPTS = "label for below sentences: \\n"

    def __init__(self):
        self.logger = setup_logger(__name__, LogsLocation.LABELLER.value)
        self.chatgpt = AutoChatGPT(logs_location=LogsLocation.LABELLER.value)

    def __save_response(self, response, filename):
        self.logger.debug(f"Saving response to {filename}")
        response = response.replace("json\n", "").replace("Copy code\n", "")
        try:
            extracted_data = [
                json.loads(json_str) for json_str in response.split("\n")
            ]
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Error occur while transforming from text to json: {e}"
            )
            return
        try:
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, "r+", encoding="utf-8") as file:
                    content = file.read()
                    if content.endswith("]"):
                        content = content[:-1] + ","
                    else:
                        content += "["

                    for item in extracted_data:
                        json_str = json.dumps(
                            item, ensure_ascii=False, indent=4
                        )
                        content += json_str + ",\n"

                    content = content.rstrip(",\n") + "]"
                    file.seek(0)
                    file.write(content)
                    file.truncate()
            else:
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(
                        extracted_data, file, ensure_ascii=False, indent=4
                    )

        except IOError as e:
            self.logger.error(f"Error occur while exporting json file: {e}")
            return
        self.logger.debug(f"Response saved at {str(datetime.now())}")

    def __label_sentences_in_specified_file(
        self, source_file, output_filename, max_retries=4
    ):
        for sent_time in range(0, 10):
            sentences_in_label_demand = read_lines_from_given_position(
                source_file, 6
            )
            prompt = Labeller.BASE_PROMPTS + sentences_in_label_demand
            retry_count = 0
            while retry_count < max_retries:
                try:
                    self.chatgpt.send_prompt_to_chatgpt(prompt)
                    response = self.chatgpt.get_chatgpt_response()
                    if response.count("{") == 6:
                        break
                except TimeoutException:
                    self.chatgpt.logger.warning(
                        f"Timeout occurred for prompt: '{prompt}'. Retrying {retry_count + 1}/{max_retries}"
                    )
                    self.chatgpt.driver.refresh()
                    time.sleep(5)
                retry_count += 1
                if retry_count == max_retries:
                    self.chatgpt.logger.error(
                        f"Failed to get response for prompt: '{prompt}' after {max_retries} retries."
                    )
                    self.chatgpt.quit()
                    return
            self.__save_response(response, output_filename)
        self.chatgpt.quit()

    def start_label(self, source_file_in_label_demand, output_filename):
        self.logger.debug(
            "Start using ChatGPT to label data from specified file"
        )
        self.__label_sentences_in_specified_file(
            source_file_in_label_demand, output_filename
        )
        self.logger.debug("Complete labelling")
