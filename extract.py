import json
import re
import string
from pathlib import Path

from constants import (
    ABBREVIATIONS, JSON_FILE,
    EXTRACTED_SUBS_DIR, JSON_SUBS_DIR,
    ORIGINAL_SUBS_DIR
)


def clean_text(text: str) -> str:
    """Apply all text cleaning functions to the given text."""
    def remove_html_elements(text: str) -> str:
        return re.sub(r'<[^>]+>', '', text)

    def expand_abbreviations(text: str) -> str:
        words = text.lower().split()
        expanded_words = [ABBREVIATIONS.get(word, word) for word in words]
        return ' '.join(expanded_words)

    def remove_punctuation(text: str) -> str:
        return text.translate(str.maketrans('', '', string.punctuation))

    text = remove_html_elements(text)
    text = expand_abbreviations(text)
    text = remove_punctuation(text)
    return text


def remove_cue_numbers(input_file: Path, output_file: Path):
    """Remove cue numbers from subtitle file."""
    with input_file.open("r", encoding="utf-8-sig") as infile, \
            output_file.open("w", encoding="utf-8") as outfile:
        for line in infile:
            if not line.strip().isdigit():
                outfile.write(line)


def srt_to_json(srt_file_path, json_file_path):
    def add_subtitle(data, temp_dict, subtitle_lines):
        if subtitle_lines:
            temp_dict['text'] = clean_text(' '.join(subtitle_lines))
            data.append(temp_dict)

    with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
        data = []
        lines = srt_file.readlines()
        temp_dict = {}
        subtitle_lines = []
        for line in lines:
            line = line.strip()

            if line.isdigit():
                # Skip the subtitle index (cue number) lines
                continue

            elif '-->' in line:
                # When a timestamp line is encountered, it means the previous subtitle has ended
                # Add the previous subtitle to the data list
                add_subtitle(data, temp_dict, subtitle_lines)
                temp_dict = {}
                subtitle_lines = []

                times = line.split(' --> ')
                temp_dict['start'] = times[0].strip()
                temp_dict['end'] = times[1].strip()

            elif line == '':
                # An empty line indicates the end of a subtitle block
                # Add the current subtitle to the data list
                add_subtitle(data, temp_dict, subtitle_lines)
                temp_dict = {}
                subtitle_lines = []

            else:
                subtitle_lines.append(clean_text(line))

        # After the loop, add the last subtitle if it hasn't been added yet
        add_subtitle(data, temp_dict, subtitle_lines)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def consolidate_json_and_cleanup():
    """Consolidate JSON files into 1.json and clean up extracted subtitles."""
    JSON_SUBS_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACTED_SUBS_DIR.mkdir(parents=True, exist_ok=True)

    # Read existing content of 1.json or create an empty dict if it doesn't exist
    if JSON_FILE.exists():
        with JSON_FILE.open("r", encoding="utf-8") as f:
            main_data = json.load(f)
    else:
        main_data = {}

    for json_file in JSON_SUBS_DIR.glob("*.json"):
        if json_file != JSON_FILE:
            movie_name = json_file.stem  # Get filename without extension
            with json_file.open("r", encoding="utf-8") as f:
                movie_data = json.load(f)

            main_data[movie_name] = movie_data
            json_file.unlink()

    # Remove all files in EXTRACTED_SUBS_DIR
    for extracted_file in EXTRACTED_SUBS_DIR.iterdir():
        extracted_file.unlink()

    # Write updated data back to 1.json
    with JSON_FILE.open("w", encoding="utf-8") as f:
        json.dump(main_data, f, indent=4)


def process_subtitle_files():
    ORIGINAL_SUBS_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACTED_SUBS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_SUBS_DIR.mkdir(parents=True, exist_ok=True)

    for sub_file in ORIGINAL_SUBS_DIR.iterdir():
        if sub_file.is_file():
            extracted_file = EXTRACTED_SUBS_DIR / sub_file.name
            json_file = JSON_SUBS_DIR / sub_file.with_suffix('.json').name
            remove_cue_numbers(sub_file, extracted_file)
            srt_to_json(extracted_file, json_file)

    consolidate_json_and_cleanup()


if __name__ == '__main__':
    process_subtitle_files()
