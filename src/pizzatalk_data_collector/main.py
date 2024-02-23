from crawler.crawler import Crawler
from generator.generator import Generator

# crawler = Crawler()
# areas = crawler.crawl("area")
# stores = crawler.crawl("store")
# categories = crawler.crawl("category")
# deals = crawler.crawl("deal")
# products = crawler.crawl("product")

generator = Generator()
generator.start_generate()
