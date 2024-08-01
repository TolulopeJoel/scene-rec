# TODO: Don't add texts with musical notes to json.

import json
import os
from pathlib import Path

from constants import (
    ORIGINAL_SUBS_DIR, JSON_FILE,
    EXTRACTED_SUBS_DIR, JSON_SUBS_DIR,
)
from utilities import rinse_text


def remove_file(file_path, downloaded_dict_path="./sources/downloaded.json"):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

    # Update the sources/downloaded.json dictionary
    with open(downloaded_dict_path, "r+", encoding="utf-8") as json_file:
        downloaded_dict = json.load(json_file)
        filename = os.path.basename(file_path).replace(".srt", "").replace(".json", "")
        if filename in downloaded_dict:
            del downloaded_dict[filename]
            json_file.seek(0)
            json.dump(downloaded_dict, json_file, ensure_ascii=False, indent=4)
            json_file.truncate()
            print(f"******* Removed {filename} from {downloaded_dict_path}")


def remove_cue_numbers(input_file: Path, output_file: Path):
    """Remove cue numbers from subtitle file."""
    try:
        with input_file.open("r", encoding="utf-8-sig", errors="replace") as infile, \
                output_file.open("w", encoding="utf-8") as outfile:
            for line in infile:
                if not line.strip().isdigit():
                    outfile.write(line)
    except UnicodeDecodeError as e:
        pass


def srt_to_json(srt_file_path, json_file_path):
    def add_subtitle(data, temp_dict, subtitle_lines):
        if subtitle_lines:
            temp_dict["text"] = rinse_text(" ".join(subtitle_lines))
            data.append(temp_dict)

    with open(srt_file_path, "r", encoding="utf-8") as srt_file:
        data = []
        lines = srt_file.readlines()
        temp_dict = {}
        subtitle_lines = []
        for line in lines:
            line = line.strip()

            if line.isdigit():
                # Skip the subtitle index (cue number) lines
                continue

            elif "-->" in line:
                # When a timestamp line is encountered, it means the previous subtitle has ended
                # Add the previous subtitle to the data list
                try:
                    add_subtitle(data, temp_dict, subtitle_lines)
                    temp_dict = {}
                    subtitle_lines = []

                    times = line.split(" --> ")
                    temp_dict["start"] = times[0].strip()
                    temp_dict["end"] = times[1].strip()
                except IndexError:
                    # files whose contents aren't SRTs (most times due to failed downloads)
                    print(f"Error processing line in file: {srt_file_path}")
                    remove_file(srt_file_path)
                    return

            elif line == "":
                # An empty line indicates the end of a subtitle block
                # Add the current subtitle to the data list
                add_subtitle(data, temp_dict, subtitle_lines)
                temp_dict = {}
                subtitle_lines = []

            else:
                subtitle_lines.append(rinse_text(line))

        add_subtitle(data, temp_dict, subtitle_lines)

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f">>>>>>> Converted {srt_file_path} to JSON")


def consolidate_json_and_cleanup():
    """Consolidate JSON files into db.json and clean up extracted subtitles."""
    JSON_SUBS_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACTED_SUBS_DIR.mkdir(parents=True, exist_ok=True)

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

    # Write updated data back to db.json
    with JSON_FILE.open("w", encoding="utf-8") as f:
        json.dump(main_data, f, indent=4)


def process_subtitle_files():
    ORIGINAL_SUBS_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACTED_SUBS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_SUBS_DIR.mkdir(parents=True, exist_ok=True)

    for sub_file in ORIGINAL_SUBS_DIR.iterdir():
        if sub_file.is_file():
            extracted_file = EXTRACTED_SUBS_DIR / sub_file.name
            json_file = JSON_SUBS_DIR / sub_file.with_suffix(".json").name
            remove_cue_numbers(sub_file, extracted_file)
            srt_to_json(extracted_file, json_file)

    consolidate_json_and_cleanup()
    print("Conversion done!")


if __name__ == "__main__":
    process_subtitle_files()
