import os
from datetime import datetime, timedelta

from crawler.crawler import Crawler
from dotenv import load_dotenv
from generator.generator import ChatGPTGenerator
from labeller.aggregator import aggregate_today_response

load_dotenv()
CHROME_PATH = os.getenv("CHROME_PATH")

# crawler = Crawler()
# areas = crawler.crawl("area")
# stores = crawler.crawl("store")
# categories = crawler.crawl("category")
# deals = crawler.crawl("deal")
# products = crawler.crawl("product")

today = datetime.now()
if today.hour == 0 and today.minute <= 10:
    yesterday = datetime.now() - timedelta(days=1)
    aggregate_today_response(yesterday.strftime("%Y%m%d"))

chatgpt = ChatGPTGenerator(chrome_path=CHROME_PATH)
chatgpt.auto_login()
chatgpt.generate_for_predefined_prompts()
