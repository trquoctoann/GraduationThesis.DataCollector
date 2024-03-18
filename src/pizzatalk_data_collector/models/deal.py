import json


class Deal:
    def __init__(
        self,
        name,
        description,
        deal_no,
        price,
        slug,
        deal_variations,
        image_path,
    ):
        self.name = name
        self.description = description
        self.deal_no = deal_no
        self.price = price
        self.slug = slug
        self.deal_variations = deal_variations
        self.image_path = image_path

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "description": self.description,
                "status": "ACTIVE",
                "dealNo": self.deal_no,
                "price": self.price,
                "slug": self.slug,
                "dealVariations": self.deal_variations,
                "imagePath": self.image_path,
            },
            ensure_ascii=False,
        )
