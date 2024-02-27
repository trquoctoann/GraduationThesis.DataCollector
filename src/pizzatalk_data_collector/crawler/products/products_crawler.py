from common.abstract_crawler import AbstractCrawler
from common.setup_logger import setup_logger
from constants.logs_location import LogsLocation
from models.option import Option
from models.option_value import OptionValue
from models.product import Product


class ProductsCrawler(AbstractCrawler):
    def __init__(self, request_url):
        super().__init__(request_url)
        self.logger = setup_logger(__name__, LogsLocation.CRAWLER.value)
        self.option_list = []
        self.option_value_list = []

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
                    original_id=product.get("id"),
                    name=product.get("name"),
                    size=product.get("productSize"),
                    slug=product.get("slug"),
                    description=product.get("shortDescription"),
                    sku=product.get("sku"),
                    price=product.get("price"),
                    image_path=self.__get_image_path(
                        product.get("productThumbnail")
                    ),
                    parent_original_id=product.get("parentId"),
                    product_variations=self.__get_product_variations_id(
                        product
                    ),
                    options=self.__get_option_and_option_value(product),
                    category_original_id=product.get("categoryId"),
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

    def __get_option_and_option_value(self, product):
        options_of_current_product = []
        for option_value in product["productOptionValues"]:
            option = option_value["option"]
            self.option_list.append(
                Option(
                    original_id=option.get("id"),
                    name=option.get("name"),
                    code=option.get("code"),
                    is_multi=option.get("isMulti"),
                    is_required=option.get("isRequired"),
                )
            )
            self.option_value_list.append(
                OptionValue(
                    original_id=option_value.get("id"),
                    value=option_value.get("value"),
                    sku=option_value.get("sku"),
                    code=option_value.get("code"),
                    uom_id=option_value.get("uomId"),
                    price=option_value.get("price"),
                    quantity=option_value.get("quantity"),
                    option_original_id=option_value.get("optionId"),
                    product_original_id=option_value.get("productId"),
                )
            )
            options_of_current_product.append(option_value.get("id"))
        return options_of_current_product

    def __get_product_variations_id(self, product):
        product_variations_id_list = []
        for variation in product["productVariations"]:
            product_variations_id_list.append(variation["id"])
        return product_variations_id_list
