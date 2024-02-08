import time

from crawler.crawler import Crawler
from generator.generator import ChatGPTGenerator
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# crawler = Crawler()
# areas = crawler.crawl("area")
# stores = crawler.crawl("store")
# categories = crawler.crawl("category")
# deals = crawler.crawl("deal")
# products = crawler.crawl("product")

retry_count = 0
while retry_count < 3:
    try:
        chatgpt = ChatGPTGenerator(
            chrome_path='"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"'
        )
        chatgpt.auto_login()
        break
    except TimeoutException:
        chatgpt.quit()
        time.sleep(5)
        retry_count += 1
chatgpt.generate_for_predefined_prompts()
