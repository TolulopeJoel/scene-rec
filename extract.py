import json
from pathlib import Path

JSON_SUBS_DIR = Path("subs/json")
ORIGINAL_SUBS_DIR = Path("subs/originals")
EXTRACTED_SUBS_DIR = Path("subs/extracted")
JSON_FILE = JSON_SUBS_DIR / "1.json"


def remove_cue_numbers(input_file: Path, output_file: Path):
    """Remove cue numbers from subtitle file."""
    with input_file.open("r", encoding="utf-8-sig") as infile, \
            output_file.open("w", encoding="utf-8") as outfile:
        for line in infile:
            if not line.strip().isdigit():
                outfile.write(line)


def srt_to_json(srt_file_path, json_file_path):
    with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
        data = []
        lines = srt_file.readlines()
        temp_dict = {}
        subtitle_lines = []

        for line in lines:
            line = line.strip()

            if line.isdigit():
                continue  # Skip subtitle index

            elif '-->' in line:
                if temp_dict:
                    # Determine if the subtitle is multi-line
                    if len(subtitle_lines) > 1:
                        temp_dict['text'] = {
                            f"line_{i+1}": text for i, text in enumerate(subtitle_lines)}
                    else:
                        temp_dict['text'] = subtitle_lines[0]
                    data.append(temp_dict)
                    temp_dict = {}
                    subtitle_lines = []

                times = line.split(' --> ')
                temp_dict['start'] = times[0].strip()
                temp_dict['end'] = times[1].strip()

            elif line == '':
                if temp_dict:
                    # Determine if the subtitle is multi-line
                    if len(subtitle_lines) > 1:
                        temp_dict['text'] = {
                            f"line_{i+1}": text for i, text in enumerate(subtitle_lines)}
                    else:
                        temp_dict['text'] = subtitle_lines[0]
                    data.append(temp_dict)
                    temp_dict = {}
                    subtitle_lines = []

            else:
                subtitle_lines.append(line)

        # Add the last subtitle if not already added
        if temp_dict:
            if len(subtitle_lines) > 1:
                temp_dict['text'] = {
                    f"line_{i+1}": text for i, text in enumerate(subtitle_lines)}
            else:
                temp_dict['text'] = subtitle_lines[0]
            data.append(temp_dict)

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

    # Process other JSON files
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
