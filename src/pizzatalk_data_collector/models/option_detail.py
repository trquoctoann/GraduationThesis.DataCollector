import json


class OptionDetail:
    def __init__(
        self,
        name,
        sku,
        code,
        uom_id,
        price,
        quantity,
    ):
        self.name = name
        self.sku = sku
        self.code = code
        self.uom_id = uom_id
        self.price = price
        self.quantity = quantity

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "sku": self.sku,
                "code": self.code,
                "uomId": self.uom_id,
                "status": "ACTIVE",
                "price": self.price,
                "quantity": self.quantity,
            },
            ensure_ascii=False,
        )
