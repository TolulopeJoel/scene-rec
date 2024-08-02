import sqlite3

from utilities import load_json

conn = sqlite3.connect('../subtitles.db')
cursor = conn.cursor()

subtitles_dataset = load_json("../media/subs/json/db.json")

# Insert data into Movies and Subtitles tables
for movie, subtitles in subtitles_dataset.items():
    cursor.execute('INSERT INTO movies (name) VALUES (?)', (movie,))
    movie_id = cursor.lastrowid
    print(f"{movie} ({movie_id}) loading to database ...")

    for subtitle in subtitles:
        try:
            cursor.execute(
                "INSERT INTO subtitles (movie_id, text, start, end) VALUES (?, ?, ?, ?)",
                (movie_id, subtitle['text'],
                 subtitle['start'], subtitle['end'])
            )
            # Insert into FTS table
            cursor.execute(
                "INSERT INTO subtitles_fts (rowid, text, movie_id) VALUES (last_insert_rowid(), ?, ?)",
                (subtitle['text'], movie_id)
            )
        except KeyError:
            pass

conn.commit()