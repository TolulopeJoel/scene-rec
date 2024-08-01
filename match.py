# TODO: expand `get_best_match` function to give user's options to choose from (simple fix)
# TODO: implement function to split user input to phrases and iterate till all matches are found.

import sqlite3

from fuzzywuzzy import process

from utilities import rinse_text


def get_movie_details(result, cursor, matched_text):
    movie_id = result[1]

    movie_query = "SELECT name FROM movies WHERE id = ?"
    cursor.execute(movie_query, (movie_id,))
    movie_name = cursor.fetchone()[0]

    sub_query = "SELECT start, end FROM subtitles WHERE movie_id = ? AND text = ?"
    cursor.execute(sub_query, (movie_id, matched_text))
    sub_start, sub_end = cursor.fetchone()

    return matched_text, movie_name, sub_start, sub_end


def get_best_match(cursor, user_input):
    """Find the best matching subtitle for the given user input."""
    rinsed_text = rinse_text(user_input)

    search_query = "SELECT text, movie_id FROM subtitles_fts WHERE text MATCH ?"
    cursor.execute(search_query, (rinsed_text,))

    if results := cursor.fetchall():
        subtitles = [result[0] for result in results]

        if best_matches := process.extractBests(rinsed_text, subtitles):
            matched_text = best_matches[0][0]
            for result in results:
                if result[0] == matched_text:
                    return get_movie_details(result, cursor, matched_text)
    return (None, None, None, None)


def main():
    conn = sqlite3.connect("./subtitles.db")
    cursor = conn.cursor()

    user_input = input("write... ")
    best_text, movie_name, start, end = get_best_match(cursor, user_input)

    if best_text:
        print(f"\n> {user_input}")
        print(f"Best matching text: {best_text}")
        print(f"Movie name: {movie_name}")
        print(f"Timestamp: {start} --> {end}")
    else:
        print("No matching subtitle found.")

    conn.close()


if __name__ == "__main__":
    while True:
        main()
