import json


class Product:
    def __init__(
        self,
        original_id,
        name,
        product_size,
        slug,
        description,
        sku,
        price,
        image_path,
        parent_original_id,
        product_variations,
        product_options,
        category_original_id,
    ):
        self.original_id = original_id
        self.name = name
        self.product_size = product_size
        self.slug = slug
        self.description = description
        self.sku = sku
        self.price = price
        self.image_path = image_path
        self.parent_original_id = parent_original_id
        self.product_variations = product_variations
        self.product_options = product_options
        self.category_original_id = category_original_id

    def to_json(self):
        return json.dumps(
            {
                "originalId": self.original_id,
                "name": self.name,
                "productSize": self.product_size,
                "slug": self.slug,
                "description": self.description,
                "sku": self.sku,
                "price": self.price,
                "imagePath": self.image_path,
                "parentOriginalId": self.parent_original_id,
                "productVariations": self.product_variations,
                "productOptions": self.product_options,
                "categoryOriginalId": self.category_original_id,
            },
            ensure_ascii=False,
        )
