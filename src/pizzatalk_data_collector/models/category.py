import json


class Category:
    def __init__(self, name, description, image_path):
        self.name = name
        self.description = description
        self.image_path = image_path

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "description": self.description,
                "status": "ACTIVE",
                "imagePath": self.image_path,
            },
            ensure_ascii=False,
        )
