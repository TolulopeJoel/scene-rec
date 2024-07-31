import json


def load_json(filename: str) -> dict:
    # try:
    with open(filename, "r") as file:
        return json.load(file)
    # except (FileNotFoundError, json.JSONDecodeError):
    #     return {}


def save_json(filename: str, data: dict) -> None:
    with open(filename, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
