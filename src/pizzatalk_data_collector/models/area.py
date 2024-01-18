import json


class Area:
    def __init__(
        self, original_id, name, code, brand_code, store_count, price_group_id
    ):
        self.original_id = original_id
        self.name = name
        self.code = code
        self.brand_code = brand_code
        self.store_count = store_count
        self.price_group_id = price_group_id

    def to_json(self):
        return json.dumps(
            {
                "originalId": self.original_id,
                "name": self.name,
                "code": self.code,
                "brandCode": self.brand_code,
                "storeCount": self.store_count,
                "priceGroupId": self.price_group_id,
            },
            ensure_ascii=False,
        )
