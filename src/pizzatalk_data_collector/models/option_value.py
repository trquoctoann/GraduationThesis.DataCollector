import json


class OptionValue:
    def __init__(
        self,
        original_id,
        value,
        sku,
        code,
        uom_id,
        price,
        quantity,
        option_original_id,
        product_original_id,
    ):
        self.original_id = original_id
        self.value = value
        self.sku = sku
        self.code = code
        self.uom_id = uom_id
        self.price = price
        self.quantity = quantity
        self.option_original_id = option_original_id
        self.product_original_id = product_original_id

    def to_json(self):
        return json.dumps(
            {
                "originalId": self.original_id,
                "value": self.value,
                "sku": self.sku,
                "code": self.code,
                "uomId": self.uom_id,
                "price": self.price,
                "quantity": self.quantity,
                "optionOriginalId": self.option_original_id,
                "productOriginalId": self.product_original_id,
            },
            ensure_ascii=False,
        )
