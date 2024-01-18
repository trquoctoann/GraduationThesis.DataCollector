import json


class Store:
    def __init__(
        self,
        original_id,
        name,
        address,
        phone_number,
        email_address,
        allow_delivery,
        allow_pickup,
        country,
        state,
        district,
        longitude,
        latitude,
        opening_hour,
        image_path,
    ):
        self.original_id = original_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email_address = email_address
        self.allow_delivery = allow_delivery
        self.allow_pickup = allow_pickup
        self.country = country
        self.state = state
        self.district = district
        self.longitude = longitude
        self.latitude = latitude
        self.opening_hour = opening_hour
        self.image_path = image_path

    def to_json(self):
        return json.dumps(
            {
                "originalId": self.original_id,
                "name": self.name,
                "address": self.address,
                "phoneNumber": self.phone_number,
                "emailAddress": self.email_address,
                "allowDelivery": self.allow_delivery,
                "allowPickup": self.allow_pickup,
                "country": self.country,
                "state": self.state,
                "district": self.district,
                "longitude": self.longitude,
                "latitude": self.latitude,
                "openingHour": self.opening_hour,
                "imagePath": self.image_path,
            },
            ensure_ascii=False,
        )
