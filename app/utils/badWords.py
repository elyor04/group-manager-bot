import os
from ..config import DATA_DIR


def get_bad_words():
    badWordsPath = os.path.join(DATA_DIR, "bad_words.txt")

    if not os.path.exists(badWordsPath):
        return []

    with open(badWordsPath, "rt") as _f:
        return _f.read().splitlines()