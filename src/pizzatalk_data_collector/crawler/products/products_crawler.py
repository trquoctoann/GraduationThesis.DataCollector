from common.abstract_crawler import AbstractCrawler
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from models.option import Option
from models.option_detail import OptionDetail
from models.product import Product


class ProductsCrawler(AbstractCrawler):
    def __init__(self, request_url):
        super().__init__(request_url)
        self.logger = setup_logger(__name__, LogsLocation.CRAWLER.value)
        self.option_list = []
        self.option_detail_list = []
        self.option_code_unique = set()

    def extract_data(self, json_response):
        result = json_response.get("result")
        if result is None:
            self.logger.debug("No result data")
            return None

        original_products = self.__extract_products(result.get("products"))
        result_products = []
        for product in original_products:
            result_products.append(
                Product(
                    name=product.get("name"),
                    size=product.get("productSize"),
                    slug=product.get("slug"),
                    description=product.get("shortDescription"),
                    sku=product.get("sku"),
                    price=product.get("price"),
                    image_path=self.__get_image_path(
                        product.get("productThumbnail")
                    ),
                    options=self.__get_option_and_option_detail(product),
                )
            )
        return result_products

    def __extract_products(self, data):
        products = []

        def recurse_items(items):
            for item in items:
                products.append(item)
                recurse_items(item["productVariations"])

        recurse_items(data)
        return products

    def __get_image_path(self, image_paths):
        image_path = image_paths.get("dir")
        if image_path:
            return "https://api.alfrescos.com.vn/uploads/images/" + image_path
        return None

    def __get_option_and_option_detail(self, product):
        options_of_current_product = []
        for option_detail in product["productOptionValues"]:
            option = option_detail["option"]
            if option.get("code") not in self.option_code_unique:
                self.option_list.append(
                    Option(
                        name=option.get("name"),
                        code=option.get("code"),
                        is_multi=option.get("isMulti"),
                        is_required=option.get("isRequired"),
                    )
                )
                self.option_code_unique.add(option.get("code"))
            self.option_detail_list.append(
                OptionDetail(
                    name=option_detail.get("value"),
                    sku=option_detail.get("sku"),
                    code=option_detail.get("code"),
                    uom_id=option_detail.get("uomId"),
                    price=option_detail.get("price"),
                    quantity=option_detail.get("quantity"),
                )
            )
            options_of_current_product.append(option_detail.get("id"))
        return options_of_current_product
