import sqlite3

conn = sqlite3.connect('../subtitles.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
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
