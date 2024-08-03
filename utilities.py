import json
import re
import string

from constants import ABBREVIATIONS


def load_json(filename: str) -> dict:
    # try:
    with open(filename, "r") as file:
        return json.load(file)
    # except (FileNotFoundError, json.JSONDecodeError):
    #     return {}


def save_json(filename: str, data: dict) -> None:
    with open(filename, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def rinse_text(text: str) -> str:
    """Apply all text cleaning functions to the given text."""
    # TODO: handle edge cases for U.S english and U.K english

    def remove_html_elements(text: str) -> str:
        return re.sub(r'<[^>]+>', "", text)

    def expand_abbreviations(text: str) -> str:
        words = text.lower().split()
        expanded_words = [ABBREVIATIONS.get(word, word) for word in words]
        return " ".join(expanded_words)

    def remove_punctuation(text: str) -> str:
        return text.translate(str.maketrans("", "", string.punctuation))

    def remove_caption_cues(text: str) -> str:
        return re.sub(r"\[(.*?)\]|\((.*?)\)", "", text)

    text = remove_caption_cues(text)
    text = remove_html_elements(text)
    text = expand_abbreviations(text)
    text = remove_punctuation(text)
    return text
