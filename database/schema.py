import sqlite3


def create_tables(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    print("Creating database tables...")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        year INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subtitles (
        id INTEGER PRIMARY KEY,
        movie_id INTEGER,
        text TEXT NOT NULL,
        start TEXT,
        end TEXT,
        FOREIGN KEY (movie_id) REFERENCES movies(id)
    )
    ''')

    cursor.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS subtitles_fts USING fts5(
        text, 
        movie_id UNINDEXED, 
        content='subtitles', 
        content_rowid='id'
    )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_subtitles_text ON subtitles(text)')

    conn.commit()
    conn.close()
    print("Creating database tables...done ✅")


if __name__ == '__main__':
    create_tables()
