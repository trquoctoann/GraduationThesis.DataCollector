from crawler.crawler import Crawler

crawler = Crawler()
# areas = crawler.crawl("area")
# stores = crawler.crawl("store")
# categories = crawler.crawl("category")
# deals = crawler.crawl("deal")
products = crawler.crawl("product")
for product in products:
    print(product.to_json())
