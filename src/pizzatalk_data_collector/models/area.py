import json


class Area:
    def __init__(self, name, code, brand_code, price_group_id):
        self.name = name
        self.code = code
        self.brand_code = brand_code
        self.price_group_id = price_group_id

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "code": self.code,
                "brandCode": self.brand_code,
                "status": "ACTIVE",
                "storeCount": 0,
                "priceGroupId": self.price_group_id,
            },
            ensure_ascii=False,
        )
