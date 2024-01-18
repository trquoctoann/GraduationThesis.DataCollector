import json


class Category:
    def __init__(self, original_id, name, description, image_path):
        self.original_id = original_id
        self.name = name
        self.description = description
        self.image_path = image_path

    def to_json(self):
        return json.dumps(
            {
                "originalId": self.original_id,
                "name": self.name,
                "description": self.description,
                "imagePath": self.image_path,
            },
            ensure_ascii=False,
        )
