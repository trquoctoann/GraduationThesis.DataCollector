import json
import os
import re
import time

from common.setup_logger import setup_logger
from constants.entities_enum import EntitiesEnum
from constants.logs_location import LogsLocation
from crawler.areas.areas_crawler import AreasCrawler
from crawler.categories.categories_crawler import CategoriesCrawler
from crawler.deals.deals_crawler import DealsCrawler
from crawler.products.products_crawler import ProductsCrawler
from crawler.stores.stores_crawler import StoresCrawler

with open(
    "src/pizzatalk_data_collector/crawler/api_source.json",
    "r",
    encoding="utf-8",
) as f:
    api_source = json.load(f)


class Crawler:
    def __init__(self, api_source=api_source):
        self.logger = setup_logger(__name__, LogsLocation.CRAWLER.value)
        self.api_source = api_source
        self.crawler = None

    def __get_urls_and_crawler(self, in_demand_entity):
        if in_demand_entity.lower() == EntitiesEnum.AREA.value:
            return self.api_source.get("area"), AreasCrawler(None)
        if in_demand_entity.lower() == EntitiesEnum.CATEGORY.value:
            return self.api_source.get("category"), CategoriesCrawler(None)
        if in_demand_entity.lower() == EntitiesEnum.DEAL.value:
            return self.api_source.get("deal"), DealsCrawler(None)
        if in_demand_entity.lower() == EntitiesEnum.STORE.value:
            return self.api_source.get("store"), StoresCrawler(None)
        if in_demand_entity.lower() == EntitiesEnum.PRODUCT.value:
            return self.api_source.get("product"), ProductsCrawler(None)
        return None, None

    def __export_json(self, in_demand_entity, url, data):
        directory_name = "crawler_result"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        export_data = []
        for each in data:
            json_object = json.loads(each.to_json())
            export_data.append(json_object)

        if in_demand_entity in ["product", "option", "option_value"]:
            file_name = in_demand_entity + re.search(
                r"GetBySlug\?slug=(.*?)&areaCode", url
            ).group(1).replace("-", "_")
        elif in_demand_entity == "store":
            file_name = in_demand_entity + re.search(
                r"areaCode=([^&]+)", url
            ).group(1)
        else:
            file_name = in_demand_entity

        with open(
            os.path.join(directory_name, file_name + ".json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(export_data, f, ensure_ascii=False, indent=4)

    def crawl(self, in_demand_entity, time_sleep=10):
        self.logger.debug(
            "Begin to crawl data for entity: " + in_demand_entity.upper()
        )
        request_urls, crawler = self.__get_urls_and_crawler(in_demand_entity)
        if request_urls is None or crawler is None:
            self.logger.debug(
                "There is no crawler for entity: " + in_demand_entity.upper()
            )
            return

        data = []
        for url in request_urls:
            crawler.request_url = url
            current_data = crawler.crawl()
            data.extend(current_data)
            if isinstance(crawler, ProductsCrawler):
                data.extend(crawler.option_list)
                data.extend(crawler.option_value_list)
                self.__export_json("option", url, crawler.option_list)
                self.__export_json(
                    "option_value", url, crawler.option_value_list
                )

            self.__export_json(in_demand_entity, url, current_data)
            time.sleep(time_sleep)

        self.logger.debug(
            "Finished crawling data for entity: " + in_demand_entity.upper()
        )
        return data
