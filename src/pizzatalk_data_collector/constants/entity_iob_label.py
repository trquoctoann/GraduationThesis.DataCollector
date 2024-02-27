from enum import Enum


class EntityIOBLabel(Enum):
    B_PIZZA = "B-Pizza"
    I_PIZZA = "I-Pizza"
    B_TOPPING = "B-Topping"
    I_TOPPING = "I-Topping"
    B_SIZE = "B-Size"
    I_SIZE = "I-Size"
    B_CRUST = "B-Crust"
    I_CRUST = "I-Crust"
    B_QUANTITY = "B-Quantity"
    I_QUANTITY = "I-Quantity"
    B_CUSTOMER_NAME = "B-Cus"
    I_CUSTOMER_NAME = "I-Cus"
    B_PHONE_NUMBER = "B-Phone"
    I_PHONE_NUMBER = "I-Phone"
    B_ADDRESS = "B-Address"
    I_ADDRESS = "I-Address"
    B_PAYMENT_METHOD = "B-Payment"
    I_PAYMENT_METHOD = "I-Payment"
    OTHER = "O"
