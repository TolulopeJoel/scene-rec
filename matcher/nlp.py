import nltk
from nltk.data import find
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize


def split_into_phrases(text: str) -> list[str]:
    """
    Split the input text into phrases based 
    on specific part-of-speech (POS) patterns.
    """
    # split into sentences, then further split by commas
    sentences = [
        sentence
        for i in sent_tokenize(text)
        for sentence in i.split(",")
    ]

    all_phrases = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)  # POS tagging

        phrases, phrase = [], []
        for index, (word, pos) in enumerate(pos_tags):
            # check if current word is a pronoun and the next word is a verb
            # if the phrase has one word, add the pronoun and verb to the phrase
            if pos == "PRP" and pos_tags[index + 1][1] == "VBZ":
                if len(phrase) == 1:
                    phrase.append(word)
                    phrase.append(pos_tags[index + 1][0])
                else:
                    phrases.append(" ".join(phrase))
                    phrase = [word, pos_tags[index + 1][0]]
                pos_tags.pop(index + 1)

            # if current word is a conjunction, number, determiner, etc., complete the current phrase
            elif pos in {"CC", "CD", "DT", "LS", "VBZ", "MD", "TO"} and phrase:
                phrases.append(" ".join(phrase))
                phrase = [word]
            else:
                phrase.append(word)

        if phrase:
            phrases.append(" ".join(phrase))

        all_phrases.extend(phrases)

    return all_phrases


def download_nltk_data():
    try:
        find('tokenizers/punkt/')
    except LookupError:
        nltk.download('punkt')

    try:
        find('chunkers/maxent_ne_chunker/')
    except LookupError:
        nltk.download('maxent_ne_chunker')

    try:
        find('corpora/words/')
    except LookupError:
        nltk.download('words')

    try:
        find('taggers/averaged_perceptron_tagger.zip')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')


if __name__ == "__main__":
    download_nltk_data()
