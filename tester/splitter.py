# TODO: first split by sentences, then by phrases

import nltk
from nltk.chunk import ne_chunk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("maxent_ne_chunker")
nltk.download("words")
nltk.download("averaged_perceptron_tagger")


def split_into_phrases(sentence):
    words = word_tokenize(sentence)
    # part of speech (pos) tagging
    pos_tags = pos_tag(words)

    # split by conjunctions, prepositions and articles
    phrases, phrase = [], []

    for word, pos in pos_tags:
        if pos in ["CC", "IN", "DT"] and phrase:
            phrases.append(" ".join(phrase))
            phrase = [word]
        else:
            phrase.append(word)

    if phrase:
        phrases.append(" ".join(phrase))

    return phrases


sentence = """
Every great achievement starts with a single step. Whether you are facing a new challenge or pursuing a long-held dream, remember that progress is built one moment, one effort at a time. Embrace each step, learn from every experience, and do not be afraid of failure it is often the greatest teacher. Believe in your abilities, stay focused on your goals, and keep pushing forward. Your dedication and perseverance will lead you to success. The journey may be tough, but it is the courage to continue that counts. You have the power to achieve greatness. Keep going!
"""
phrases = split_into_phrases(sentence)
print(phrases)


# two part of speeches i need to looke out for:
# adverb: RB
# adjective: JJ
