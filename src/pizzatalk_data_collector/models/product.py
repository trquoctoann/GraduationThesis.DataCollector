import json


class Product:
    def __init__(
        self,
        name,
        size,
        slug,
        description,
        sku,
        price,
        image_path,
        options,
    ):
        self.name = name
        self.size = size
        self.slug = slug
        self.description = description
        self.sku = sku
        self.price = price
        self.image_path = image_path
        self.options = options

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "size": self.size,
                "slug": self.slug,
                "description": self.description,
                "sku": self.sku,
                "status": "ACTIVE",
                "imagePath": self.image_path,
                "price": self.price,
                "options": self.options,
            },
            ensure_ascii=False,
        )
