import json


class EntityRecognitionData:
    def __init__(self, words, pos, label):
        self.words = words
        self.pos = pos
        self.label = label

    def to_json(self):
        return json.dumps(
            {"words": self.words, "pos": self.pos, "label": self.label},
            ensure_ascii=False,
        )
