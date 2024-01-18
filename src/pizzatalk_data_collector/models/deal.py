import json


class Deal:
    def __init__(
        self,
        original_id,
        name,
        description,
        deal_no,
        price,
        slug,
        deal_variations,
        original_parent_id,
        image_path,
    ):
        self.original_id = original_id
        self.name = name
        self.description = description
        self.deal_no = deal_no
        self.price = price
        self.slug = slug
        self.deal_variations = deal_variations
        self.original_parent_id = original_parent_id
        self.image_path = image_path

    def to_json(self):
        return json.dumps(
            {
                "originalId": self.original_id,
                "name": self.name,
                "description": self.description,
                "dealNo": self.deal_no,
                "price": self.price,
                "slug": self.slug,
                "dealVariations": self.deal_variations,
                "originalParentId": self.original_parent_id,
                "imagePath": self.image_path,
            },
            ensure_ascii=False,
        )
