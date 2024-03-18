from common.abstract_crawler import AbstractCrawler
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from models.category import Category


class CategoriesCrawler(AbstractCrawler):
    def __init__(self, request_url):
        super().__init__(request_url)
        self.logger = setup_logger(__name__, LogsLocation.CRAWLER.value)

    def extract_data(self, json_response):
        result = json_response.get("result")
        if result is None:
            self.logger.debug("No result data")
            return None

        original_categories = result.get("categories")
        result_categories = []
        for category in original_categories:
            result_categories.append(
                Category(
                    name=category.get("name"),
                    description=category.get("shortDescription"),
                    image_path=self.__get_image_path(
                        category.get("imagePaths")
                    ),
                )
            )
        return result_categories

    def __get_image_path(self, image_paths):
        image_path = image_paths.get("dir")
        if image_path:
            return "https://api.alfrescos.com.vn/uploads/images/" + image_path
        return None
