from database.load import insert_subtitles_data
from database.schema import create_tables
from matcher.nlp import download_nltk_data

if __name__ == "__main__":
    create_tables("subtitles.db")
    download_nltk_data()
    insert_subtitles_data("subtitles.db", "db.json")
