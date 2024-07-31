import requests
from tqdm import tqdm

from constants import ADDICTIVE_COOKIES, ADDICTIVE_HEADERS
from utilities import load_json, save_json


def download_subtitle(title: str, sub_url: str, MOVIES) -> None:
    try:
        response = requests.get(
            sub_url,
            headers=ADDICTIVE_HEADERS,
            cookies=ADDICTIVE_COOKIES
        )

        with open(f"../media/subs/originals/{title}.srt", "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

        downloaded_movies[title] = sub_url
    except:
        save_json("downloaded.json", downloaded_movies)
        return  # skip file download


def get_unsaved_subs() -> dict:
    all_subs = load_json("movies.json")
    saved_subs = load_json("downloaded.json")

    movie_titles = set(all_subs.keys())
    downloaded_titles = set(saved_subs.keys())
    missing_titles = movie_titles - downloaded_titles

    return {title: all_subs[title] for title in sorted(missing_titles)}


if __name__ == "__main__":
    missing_subs = get_unsaved_subs()
    downloaded_movies = load_json("downloaded.json")

    for title, url in missing_subs.items():
        download_subtitle(title, url, downloaded_movies)

    save_json("downloaded.json", downloaded_movies)
