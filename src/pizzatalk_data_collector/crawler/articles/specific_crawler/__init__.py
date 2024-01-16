from .bulinews_crawler import BulinewsCrawler
from .cultofcalcio_crawler import CultofcalcioCrawler
from .europe_articles_crawler import EuropeArticlesCrawler
from .fotmob_crawler import FotmobCrawler
from .ninety_min_crawler import NinetyMinCrawler
from .skysports_crawler import SkySportsCrawler

# A registry that maps source identifiers to crawler classes
CRAWLER_IDENTIFIER = {
    "www.fotmob.com": "FotmobCrawler",
    "www.90min.com": "NinetyMinCrawler",
    "www.skysports.com": "SkySportsCrawler",
    "bulinews.com": "BulinewsCrawler",
    "cultofcalcio.com": "CultofcalcioCrawler",
    "getfootballnewsbene.com": "EuropeArticlesCrawler",
    "getfootballnewsspain.com": "EuropeArticlesCrawler",
    "www.getfootballnewsgermany.com": "EuropeArticlesCrawler",
    "www.getfootballnewsitaly.com": "EuropeArticlesCrawler",
    "www.getfootballnewsfrance.com": "EuropeArticlesCrawler",
}

CRAWLER_REGISTRY = {
    "FotmobCrawler": FotmobCrawler,
    "NinetyMinCrawler": NinetyMinCrawler,
    "SkySportsCrawler": SkySportsCrawler,
    "BulinewsCrawler": BulinewsCrawler,
    "CultofcalcioCrawler": CultofcalcioCrawler,
    "EuropeArticlesCrawler": EuropeArticlesCrawler,
}

NATION_REGISTRY = {
    "getfootballnewsbene.com": "belgium",
    "getfootballnewsspain.com": "spain",
    "www.getfootballnewsgermany.com": "germany",
    "www.getfootballnewsitaly.com": "italy",
    "www.getfootballnewsfrance.com": "france",
}
