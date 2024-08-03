# TODO: implement function to split user input to phrases and iterate till all matches are found.
import sqlite3

from utilities import rinse_text


def get_movie_details(result, cursor):
    matched_text, movie_id = result[0], result[1]

    movie_query = "SELECT name FROM movies WHERE id = ?"
    cursor.execute(movie_query, (movie_id,))
    movie_name = cursor.fetchone()[0]

    sub_query = "SELECT start, end FROM subtitles WHERE movie_id = ? AND text = ?"
    cursor.execute(sub_query, (movie_id, matched_text))
    sub_start, sub_end = cursor.fetchone()

    return matched_text, movie_name, sub_start, sub_end


def fetch_subtitles(cursor, rinsed_text, limit=None):
    search_query = """
    SELECT text, movie_id, bm25(subtitles_fts) AS score 
    FROM subtitles_fts WHERE text MATCH ? ORDER BY score
    """
    if limit:
        search_query += " LIMIT ?"
        cursor.execute(search_query, (rinsed_text, limit))
    else:
        cursor.execute(search_query, (rinsed_text,))

    return cursor.fetchall()


def get_best_match(cursor, user_input, max_matches=10):
    """Find the best matching subtitle for the given user input."""
    if results := fetch_subtitles(cursor, rinse_text(user_input), max_matches):
        return (get_movie_details(result, cursor) for result in results)
    return ((None, None, None, None),)


def main(cursor, user_input):
    best_matches = get_best_match(cursor, user_input)

    print(f"\n> {user_input}")
    for best_text, movie_name, start, end in best_matches:
        if best_text:
            print(f"\nBest matching text: {best_text}")
            print(f"Movie name: {movie_name}")
            print(f"Timestamp: {start} --> {end}")
        else:
            print("No matching subtitle found.")


if __name__ == "__main__":
    conn = sqlite3.connect("./subtitles.db")
    cursor = conn.cursor()
    user_input = input("write... ")
    main(cursor, user_input)
    conn.close()
