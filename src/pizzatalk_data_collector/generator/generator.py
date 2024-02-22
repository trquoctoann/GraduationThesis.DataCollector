import os
from datetime import datetime, timedelta

from common.auto_chatgpt import AutoChatGPT
from dotenv import load_dotenv
from generator.aggregate_generator_result import (
    aggregate_specified_date_response,
)

load_dotenv()
CHROME_PATH = os.getenv("CHROME_PATH")

prompts = [
    [
        "Suppose you are a customer wanting to order pizza online. Create 15 text messages to the shop to place your order. The sentence format should be compatible with the entity recognition model.",
        10,
    ]
]


def using_chatgpt_to_generate_data():
    today = datetime.now()
    if today.hour == 0 and today.minute == 0:
        yesterday = datetime.now() - timedelta(days=1)
        aggregate_specified_date_response(yesterday.strftime("%Y%m%d"))

    chatgpt = AutoChatGPT(chrome_path=CHROME_PATH)
    chatgpt.generate_for_predefined_prompts(prompts)
