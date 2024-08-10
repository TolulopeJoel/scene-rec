import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

from match import get_best_match
from phrase_splitter import split_into_phrases
from utilities import rinse_text

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])


def get_db_connection():
    conn = sqlite3.connect("./subtitles.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/matchs', methods=['POST'])
def get_subtitles():
    data = request.get_json()
    user_input = data.get('text', '')
    limit = data.get('limit', 5)

    if not user_input:
        return jsonify({
            'error': 'Expected a non-empty "text" field in the request data.',
            'expected': {
                'text': 'string',
                'limit': 'integer (optional, default: 5)'
            }
        }), 400

    all_phrases = split_into_phrases(rinse_text(user_input))
    results = []

    conn = get_db_connection()
    cursor = conn.cursor()

    for phrase in all_phrases:
        phrase_matches = get_best_match(cursor, phrase, limit)

        phrase_result = {
            'phrase': phrase,
            'matches': [
                {
                    'movie': movie,
                    'text': subtitle,
                    'timestamp_start': time_start,
                    'timestamp_end': time_end
                }
                for subtitle, movie, time_start, time_end in phrase_matches
                if subtitle
            ]
        }

        results.append(phrase_result)

    conn.close()

    response = {
        'phrases': len(all_phrases),
        'results': results
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
