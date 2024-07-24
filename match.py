"""
Match user input to subtitles and return the movie info
"""

import json
from pathlib import Path


def flatten_subtitle_text(text):
    if isinstance(text, dict):
        return ' '.join(text.values())
    return text


def jaccard_similarity(str1, str2):
    set1 = set(str1.split())
    set2 = set(str2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0


def find_best_match(user_input, subtitles_data):
    matches = []
    for movie, subtitles in subtitles_data.items():
        for subtitle in subtitles:
            subtitle_text = flatten_subtitle_text(subtitle['text'])
            if "♪" not in subtitle_text:  # Exclude subtitles with musical notes
                similarity = jaccard_similarity(
                    user_input.lower(), subtitle_text.lower())
                if similarity > 0:
                    matches.append({
                        'movie': movie,
                        'text': subtitle_text,
                        'start': subtitle['start'],
                        'end': subtitle['end'],
                        'similarity': similarity,
                        'phrase': user_input
                    })
    if matches:
        # Sort matches based on the similarity score
        sorted_matches = sorted(
            matches, key=lambda x: x['similarity'], reverse=True)
        # Return the best match and all matches for further use
        return sorted_matches[0], sorted_matches
    return None, None  # Will be None if no matches found


def find_remaining_phrases(user_input, subtitles_data):
    original_input = user_input.lower().split()
    found_phrases = []
    matched_texts = set()
    while len(original_input) > 1:  # Ensure we have at least two words to form a phrase
        current_input = ' '.join(original_input)
        match, _ = find_best_match(current_input, subtitles_data)
        if match and match['text'] not in matched_texts:
            found_phrases.append(match)
            matched_texts.add(match['text'])
            # Remove matched words from the original input
            matched_words = set(match['text'].lower().split())
            original_input = [
                word for word in original_input if word not in matched_words]
        else:
            # Remove the last word to try to match the remaining phrase
            original_input.pop()
    return found_phrases


def sort_matches_by_input_order(matches, user_input):
    input_words = user_input.split()
    input_phrases = [' '.join(input_words[i:j]) for i in range(
        len(input_words)) for j in range(i+2, len(input_words)+1)]
    sorted_matches = []
    for phrase in input_phrases:
        for match in matches:
            if phrase in match['text'].lower() and match not in sorted_matches:
                sorted_matches.append(match)
                break
    return sorted_matches


def load_subtitles(json_file_path):
    with json_file_path.open('r', encoding='utf-8') as file:
        return json.load(file)


def find_sorted_matching_phrases(user_input: int) -> dict:
    JSON_FILE = Path("subs/json/1.json")
    subtitles_data = load_subtitles(JSON_FILE)

    matching_phrases = find_remaining_phrases(
        user_input.lower(), subtitles_data)

    if matching_phrases:
        sorted_phrases = sort_matches_by_input_order(
            matching_phrases, user_input.lower())
        return sorted_phrases
    return "No matching phrases found."
