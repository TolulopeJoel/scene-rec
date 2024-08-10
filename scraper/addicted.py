# gets new movies from addicted, and update the movies json
# TODO: add movie genres
import requests
from bs4 import BeautifulSoup

from constants import ADDICTIVE_BASE_URL, ADDICTIVE_COOKIES, ADDICTIVE_HEADERS
from utils import load_json, save_json


def is_ascii(title: str) -> bool:
    return all(ord(char) < 128 for char in title)


def extract_movie_info(movie) -> tuple[str, str]:
    title = ' '.join(movie.text.strip().split())
    movie_id = movie.a['href'].split("/")[-1]
    download_url = f"{ADDICTIVE_BASE_URL}/original/{movie_id}/0"
    return title, download_url


def update_movies(movies: list) -> None:
    movie_data = load_json("movies.json")
    other_data = load_json("non_english.json")

    for movie in movies:
        title, download_url = extract_movie_info(movie)
        if is_ascii(title):
            movie_data[title] = download_url
        else:
            other_data[title] = download_url

    save_json("movies.json", movie_data)
    save_json("non_english.json", other_data)


def main() -> None:
    addicted_page = requests.get(
        f"{ADDICTIVE_BASE_URL}/movie-subtitles",
        headers=ADDICTIVE_HEADERS,
        cookies=ADDICTIVE_COOKIES
    )
    soup = BeautifulSoup(addicted_page.text, "lxml")
    update_movies(soup.find_all("h3"))


if __name__ == '__main__':
    main()
