import json


class Option:
    def __init__(self, name, code, is_multi, is_required):
        self.name = name
        self.code = code
        self.is_multi = is_multi
        self.is_required = is_required

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "code": self.code,
                "status": "ACTIVE",
                "isMulti": self.is_multi,
                "isRequired": self.is_required,
            },
            ensure_ascii=False,
        )
