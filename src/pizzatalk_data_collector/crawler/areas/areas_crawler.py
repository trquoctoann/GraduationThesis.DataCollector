from common.abstract_crawler import AbstractCrawler
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from models.area import Area


class AreasCrawler(AbstractCrawler):
    def __init__(self, request_url):
        super().__init__(request_url)
        self.logger = setup_logger(__name__, LogsLocation.CRAWLER.value)

    def extract_data(self, json_response):
        result = json_response.get("result")
        if result is None:
            self.logger.debug("No result data")
            return None

        original_store_areas = result.get("storeArea")
        result_areas = []
        for area in original_store_areas:
            result_areas.append(
                Area(
                    original_id=area.get("id"),
                    name=area.get("name"),
                    code=area.get("code"),
                    brand_code=area.get("brandCode"),
                    store_count=area.get("storeCount"),
                    price_group_id=area.get("priceGroupId"),
                )
            )
        return result_areas
