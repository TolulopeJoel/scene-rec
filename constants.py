import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

JSON_SUBS_DIR = Path("./media/subs/json")
ORIGINAL_SUBS_DIR = Path("./media/subs/originals")
EXTRACTED_SUBS_DIR = Path("./media/subs/extracted")
JSON_FILE = Path("./media/subs/db.json")

ABBREVIATIONS = {
    "i'll": "i will",
    "can't": "cannot",
    "won't": "will not",
    "it's": "it is",
    "don't": "do not",
    "i'm": "i am",
    "you're": "you are",
    "they're": "they are",
    "we're": "we are",
    "he's": "he is",
    "she's": "she is",
    "that's": "that is",
    "there's": "there is",
    "what's": "what is",
    "who's": "who is",
    "doesn't": "does not",
    "didn't": "did not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "hasn't": "has not",
    "haven't": "have not",
    "hadn't": "had not",
    "couldn't": "could not",
    "shouldn't": "should not",
    "wouldn't": "would not",
    "mightn't": "might not",
    "mustn't": "must not",
    "needn't": "need not",
    "oughtn't": "ought not",
    "shan't": "shall not",
    "how's": "how is",
    "here's": "here is",
    "where's": "where is",
    "why's": "why is",
    "i'd": "i would",
    "you'd": "you would",
    "he'd": "he would",
    "she'd": "she would",
    "we'd": "we would",
    "they'd": "they would",
    "i've": "i have",
    "you've": "you have",
    "we've": "we have",
    "they've": "they have",
    "should've": "should have",
    "would've": "would have",
    "could've": "could have",
    "might've": "might have",
    "must've": "must have",
    "let's": "let us",
    "ma'am": "madam",
    "o'clock": "of the clock",
    "ne'er": "never",
    "y'all": "you all",
    "c'mon": "come on",
    "lotta": "lot of",
    "dunno": "do not know",
    "ain't": "aint",
    "y'know": "you know",
    "watcha": "what are you",
    "d'you": "do you",
    "d'ya": "do you",
    "cuz": "because",
    "goin'": "going",
    "comin'": "coming",
    "talkin'": "talking",
    "lookin'": "looking",
    "runnin'": "running",
    "walkin'": "walking",
    "nothin'": "nothing",
    "somethin'": "something",
    "everythin'": "everything",
    "anythin'": "anything",
    "gimme": "give me",
    "whatcha": "what are you",
    "doin'": "doing",
    "hafta": "have to",
    "y'got": "you got",
    "y'want": "you want",
    "oughta": "ought to",
    "tryna": "trying to",
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "got to",
    "lemme": "let me",
    "kinda": "kind of",
    "sorta": "sort of",
    "outta": "out of",
    "gotcha": "got you",
    "betcha": "bet you",
    "woulda": "would have",
    "coulda": "could have",
    "shoulda": "should have",
    "mighta": "might have",
    "wouldn'ta": "would not have",
    "couldn'ta": "could not have",
    "shouldn'ta": "should not have",
    "mightn'ta": "might not have",
    "ain'tcha": "are not you",
    "aren'tcha": "are not you",
    "isn'tcha": "is not you",
    "wasn'tcha": "was not you",
    "weren'tcha": "were not you",
    "hasn'tcha": "has not you",
    "haven'tcha": "have not you",
    "hadn'tcha": "had not you",
    "don'tcha": "do not you",
    "doesn'tcha": "does not you",
    "didn'tcha": "did not you",
    "won'tcha": "will not you",
    "wouldn'tcha": "would not you",
    "couldn'tcha": "could not you",
    "shouldn'tcha": "should not you",
    "mightn'tcha": "might not you",
    "mustn'tcha": "must not you",
    "oughtn'tcha": "ought not you",
    "needn'tcha": "need not you",
    "daren'tcha": "dare not you",
    "hadn't've": "had not have",
    "wouldn't've": "would not have",
    "couldn't've": "could not have",
    "shouldn't've": "should not have",
    "mightn't've": "might not have",
    "mustn't've": "must not have",
}

# SCRAPING DEETS
ADDICTIVE_HEADERS = {
    'User-Agent': os.getenv('ADDICTIVE_USER_AGENT'),
    'Accept': os.getenv('ADDICTIVE_ACCEPT'),
    'Accept-Language': os.getenv('ADDICTIVE_ACCEPT_LANGUAGE'),
    'Accept-Encoding': os.getenv('ADDICTIVE_ACCEPT_ENCODING'),
    'Connection': os.getenv('ADDICTIVE_CONNECTION'),
    'Upgrade-Insecure-Requests': os.getenv('ADDICTIVE_UPGRADE_INSECURE_REQUESTS'),
    'Sec-Fetch-Dest': os.getenv('ADDICTIVE_SEC_FETCH_DEST'),
    'Sec-Fetch-Mode': os.getenv('ADDICTIVE_SEC_FETCH_MODE'),
    'Sec-Fetch-Site': os.getenv('ADDICTIVE_SEC_FETCH_SITE'),
    'Priority': os.getenv('ADDICTIVE_PRIORITY'),
    'TE': os.getenv('ADDICTIVE_TE')
}
ADDICTIVE_COOKIES = {
    '__utma': os.getenv('ADDICTIVE__UTMA'),
    '__utmz': os.getenv('ADDICTIVE__UTMZ'),
    'wikisubtitlesuser': os.getenv('ADDICTIVE_WIKISUBTITLESUSER'),
    'wikisubtitlespass': os.getenv('ADDICTIVE_WIKISUBTITLESPASS'),
    'PHPSESSID': os.getenv('ADDICTIVE_PHPSESSID'),
    '__utmb': os.getenv('ADDICTIVE__UTMB'),
    '__utmc': os.getenv('ADDICTIVE__UTMC'),
    '__utmt': os.getenv('ADDICTIVE__UTMT'),
    'xpMenuCookv2': os.getenv('ADDICTIVE_XP_MENU_COOKV2')
}
ADDICTIVE_BASE_URL = os.getenv('ADDICTIVE_BASE_URL')
