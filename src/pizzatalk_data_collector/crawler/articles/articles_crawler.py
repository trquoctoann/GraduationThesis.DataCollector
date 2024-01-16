from datetime import timedelta
from urllib.parse import urlparse

from crawler.articles.collect_crawlable_link import collect_crawlable_link
from crawler.articles.specific_crawler import (
    CRAWLER_IDENTIFIER,
    CRAWLER_REGISTRY,
    NATION_REGISTRY,
)
from crawler.articles.specific_crawler.abstract_crawler import (
    AbstractArticleCrawler,
)
from crawler.articles.specific_crawler.europe_articles_crawler import (
    EuropeArticlesCrawler,
)
from crawler.articles.utils.date_utils import (
    convert_datetext_to_datetime,
    get_current_time,
)
from utils.setup_logger import setup_logger

fotmob_sources_list = [
    "https://www.fotmob.com/en-GB/leagues/47/news/premier-league",
    "https://www.fotmob.com/en-GB/leagues/42/news/champions-league",
    "https://www.fotmob.com/en-GB/leagues/87/news/laliga",
    "https://www.fotmob.com/en-GB/leagues/54/news/bundesliga",
    "https://www.fotmob.com/en-GB/leagues/55/news/serie",
    "https://www.fotmob.com/en-GB/leagues/53/news/ligue-1",
    "https://www.fotmob.com/en-GB/leagues/73/news/europa-league",
    "https://www.fotmob.com/en-GB/leagues/77/news/world-cup",
    "https://www.fotmob.com/en-GB/leagues/132/news/fa-cup",
    "https://www.fotmob.com/en-GB/leagues/50/news/euro",
]


class ArticlesCrawler:
    def __init__(self, fotmob_sources_list=fotmob_sources_list):
        self.fotmob_sources_list = fotmob_sources_list
        self.logger = setup_logger(__name__)
        self.last_crawl_time = self.__get_last_time_crawl()
        self.articles_link_list = self.__collect_crawl_links()
        self.crawler_instances = {}

    def __get_last_time_crawl(self):
        file_path = "src/data_crawler/crawler/articles/last_time_crawl.txt"
        try:
            with open(file_path, "r") as file:
                datetime_str = file.readline().strip()
            self.logger.debug(
                f"Extracted successfully, last crawl time: {datetime_str}"
            )
            return convert_datetext_to_datetime(datetime_str)
        except Exception as e:
            self.logger.error(
                f"Error reading last time crawl from file: {e}", exc_info=True
            )
            return get_current_time() - timedelta(days=1)

    def __save_new_last_time_crawl(self):
        crawl_time = get_current_time()
        file_path = "src/data_crawler/crawler/articles/last_time_crawl.txt"
        try:
            with open(file_path, "w") as file:
                file.write(crawl_time.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            self.logger.error(
                f"Error saving new last crawl time to file: {e}", exc_info=True
            )

    def __collect_crawl_links(self):
        try:
            articles_link_list = collect_crawlable_link(
                self.last_crawl_time, self.fotmob_sources_list
            )
            return [link for sublist in articles_link_list for link in sublist]
        except Exception as e:
            self.logger.error(
                f"Error collecting crawl links: {e}", exc_info=True
            )
            return []

    def __select_crawler(self, url):
        self.logger.debug(f"Selecting crawler for: {url}")
        url = AbstractArticleCrawler.get_90min_link(url)
        domain = urlparse(url).netloc

        crawler_identifier = CRAWLER_IDENTIFIER.get(domain)
        if not crawler_identifier:
            self.logger.debug(f"No crawler found for url: {url}")
            return None

        crawler = self.crawler_instances.get(crawler_identifier)
        if not crawler:
            crawler_class = CRAWLER_REGISTRY.get(crawler_identifier)
            crawler = crawler_class(None)
            self.crawler_instances[crawler_identifier] = crawler

        if isinstance(crawler, EuropeArticlesCrawler):
            nation = NATION_REGISTRY.get(domain)
            crawler.nation = nation

        crawler.source_url = url
        self.logger.debug(
            f"Successfully selected crawler {type(crawler)} for source: {url}"
        )

        return crawler

    def __filter_articles_by_time(self, articles):
        result = []
        for article in articles:
            if article:
                published_date = convert_datetext_to_datetime(
                    article.published_date
                )
                if self.last_crawl_time < published_date:
                    result.append(article)
        return result

    def crawl(self):
        self.logger.debug("Beginning to crawl for articles")
        articles = []
        for article_link in self.articles_link_list:
            crawler = self.__select_crawler(article_link)
            if crawler is None:
                continue

            try:
                article_data = crawler.crawl()
                articles.append(article_data)
            except Exception as e:
                self.logger.error(
                    "Error crawling URL {}: {}".format(article_link, e),
                    exc_info=True,
                )
        result = self.__filter_articles_by_time(articles)
        self.__save_new_last_time_crawl()
        self.logger.debug("Finished crawling articles")
        return result
