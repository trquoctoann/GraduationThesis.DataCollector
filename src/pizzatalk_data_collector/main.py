from crawler.crawler import Crawler
from generator.generator import ChatGPTGenerator

crawler = Crawler()
areas = crawler.crawl("area")
stores = crawler.crawl("store")
categories = crawler.crawl("category")
deals = crawler.crawl("deal")
products = crawler.crawl("product")


# chatgpt = ChatGPTGenerator(
#     chrome_path='"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'
# )

# prompts = [
#     "Cho tôi 10 câu về đặt bánh pizza",
#     "Cho tôi 10 câu reply của shop",
#     "Tiếp",
# ]
# chatgpt.generate_for_predefined_prompts(prompts)
