from common.abstract_crawler import AbstractCrawler
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from models.deal import Deal


class DealsCrawler(AbstractCrawler):
    def __init__(self, request_url):
        super().__init__(request_url)
        self.logger = setup_logger(__name__, LogsLocation.CRAWLER.value)

    def extract_data(self, json_response):
        result = json_response.get("result")
        if result is None:
            self.logger.debug("No result data")
            return None

        original_deals = self.__extract_deals(result.get("deals"))
        result_deals = []
        for deal in original_deals:
            result_deals.append(
                Deal(
                    original_id=deal.get("id"),
                    name=deal.get("name"),
                    description=deal.get("description"),
                    deal_no=deal.get("dealNo"),
                    price=deal.get("dealPrice"),
                    slug=deal.get("slug"),
                    deal_variations=self.__get_deal_variations_id(deal),
                    original_parent_id=deal.get("parentId"),
                    image_path=self.__get_image_path(deal.get("dealImage")),
                )
            )
        return result_deals

    def __extract_deals(self, data):
        deals = []

        def recurse_items(items, parent_id):
            for item in items:
                item["parentId"] = parent_id
                deals.append(item)
                recurse_items(item["dealVariations"], item.get("id"))

        recurse_items(data, None)
        return deals

    def __get_image_path(self, image_paths):
        image_path = image_paths.get("dir")
        if image_path:
            return "https://api.alfrescos.com.vn/uploads/images/" + image_path
        return None

    def __get_deal_variations_id(self, deal):
        deal_variations_id_list = []
        for variation in deal["dealVariations"]:
            deal_variations_id_list.append(variation["id"])
        return deal_variations_id_list
