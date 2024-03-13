import json
import re

from constants.entity_iob_label import EntityIOBLabel


def process_sentence(sentence):
    tokens = re.findall(r"[\w']+|[.,!?;]", sentence)
    return {
        "words": tokens,
        "label": [EntityIOBLabel.OTHER.value] * len(tokens),
    }


file_path = "conversations\\order\\ideal_order.txt"
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

sentences = content.split("\n")

list_of_objects = [
    process_sentence(sentence) for sentence in sentences if sentence
]

json_content = json.dumps(list_of_objects, ensure_ascii=False, indent=4)

json_file_path = "conversations\\order\\ideal_order.json"
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json_file.write(json_content)
