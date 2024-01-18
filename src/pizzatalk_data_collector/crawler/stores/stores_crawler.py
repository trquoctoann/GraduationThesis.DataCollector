from common.abstract_crawler import AbstractCrawler
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from models.store import Store


class StoresCrawler(AbstractCrawler):
    def __init__(self, request_url):
        super().__init__(request_url)
        self.logger = setup_logger(__name__, LogsLocation.CRAWLER.value)

    def extract_data(self, json_response):
        result = json_response.get("result")
        if result is None:
            self.logger.debug("No result data")
            return None

        original_stores = result.get("stores")
        result_stores = []
        for store in original_stores:
            result_stores.append(
                Store(
                    original_id=store.get("id"),
                    name=store.get("name"),
                    address=store.get("address"),
                    phone_number=store.get("phoneNumber"),
                    email_address=store.get("emailAddress"),
                    allow_delivery=store.get("allowDelivery"),
                    allow_pickup=store.get("allowPickup"),
                    country=store.get("country"),
                    state=store.get("states"),
                    district=store.get("district"),
                    longitude=store.get("longitude"),
                    latitude=store.get("latitude"),
                    opening_hour=store.get("openingHourDisplay"),
                    image_path=store.get("imageDisplay"),
                )
            )
        return result_stores
