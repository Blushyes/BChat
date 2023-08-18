import json


def save_json(name, info):
    with open(name, 'w') as f:
        json.dump(info, f, ensure_ascii=False)
