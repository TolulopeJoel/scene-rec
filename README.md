# SceneRec

## Project Description

SceneRec is an NLP (Natural Language Processing) tool that lets users get movie clip recommendations for phrases or sentences. It intelligently matches user inputs to complete sentences spoken in various movie scenes. SceneRec saves time and effort for editors, content creators, and video enthusiasts.

## Motivation

The idea for this project was born from a moment of realisation while watching a [video](https://www.instagram.com/p/C8UYQkXR8Zd/) on Instagram. I couldn't help but think about the huge effort it must have taken for the editor to find and stitch together movie scenes that matched specific phrases. 

Manually filtering through countless films to find the right words is overwhelming and extremely time-consuming.

This tool aims to make the creative process more efficient, enabling editors, content creators, and video enthusiasts to bring their ideas to life with few keystrokes. In the future, the software will be able to create a video from the default recommended scenes automatically.


## Features

- Efficient phrase-to-scene matching
- Support for multiple movies and TV shows
- Customizable search results
- API for easy integration into existing workflows

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tolulopejoel/scene-rec.git
   cd scene-rec
   ```

2. **Set Up the Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```


## Usage

1. **Prepare Subtitles Database**:
   
   Option A: Download Pre-Filled Subtitles JSON File
   - Download [db.json](https://drive.google.com/file/d/1swANoP9PdFRrCLuzkWM9PSy0q7JWbzzD/view?usp=drivesdk) and place it in the project root.
   - Run the following commands:
     ```bash
     cd database
     python schema.py
     python load.py
     ```

   Option B: Scrape Your Own Subtitles
   - Scrape subtitles from your own sources, then place subtitle files in `media/subs/originals`
   - Run the following commands:
     ```bash
     cd scraper
     python extract.py
     cd ../database
     python schema.py
     python load.py
     ```

2. **Start the API**:
   ```bash
   python api.py
   ```

3. **Use the API**:
   The API will be available at `http://127.0.0.1:5000/`.


4. **`/search`** (POST): Search for movie clips by providing a phrase or sentence.

    **Request Body**:
    ```json
    {
        "text": "wait till i can do anything",
        "limit": 3
    }
    ```

    **Response**:
    ```json
    {
        "phrases": 2,
        "results": [
            {
                "phrase": "wait till i",
                "matches": [
                    {
                        "movie": "The Boy(In a Dark Place) (2016)",
                        "text": "wait till i tell daddy",
                        "timestamp_start": "00:17:34,511",
                        "timestamp_end": "00:17:36,687"
                    },
                    {
                        "movie": "Nomis (2018)",
                        "text": "wait till i fall asleep",
                        "timestamp_start": "00:31:01,959",
                        "timestamp_end": "00:31:03,600"
                    },
                    {
                        "movie": "Love Thy Neighbour (1973)",
                        "text": "wait till i see jacko",
                        "timestamp_start": "00:57:01,752",
                        "timestamp_end": "00:57:02,913"
                    },
                ]
            },
            {
                "phrase": "can do anything",
                "matches": [
                    {
                        "movie": "Janis: Little Girl Blue [Janis] (2015)",
                        "text": "anything i can do anything i can do",
                        "timestamp_start": "00:02:32,138",
                        "timestamp_end": "00:02:38,020",
                    },
                    {
                        "movie": "Legion Of Super-Heroes (2023)",
                        "text": "i can do anything",
                        "timestamp_start": "00:49:56,995",
                        "timestamp_end": "00:49:59,164"
                    },
                    {
                        "movie": "Le Mur de l'Atlantique [Atlantic Wall] (1970)",
                        "text": "you can do anything tell anything",
                        "timestamp_start": "00:44:11,660",
                        "timestamp_end": "00:44:14,219"
                    }
                ]
            }
        ]
    }
    ```

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
