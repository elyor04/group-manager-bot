import os
from app.config import DATA_DIR


def get_bad_words():
    badWordsPath = os.path.join(DATA_DIR, "bad-words.txt")

    if not os.path.exists(badWordsPath):
        return []

    with open(badWordsPath, "rt") as _f:
        return _f.read().splitlines()
