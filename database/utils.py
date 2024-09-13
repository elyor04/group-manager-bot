import os


def get_bad_words():
    if not os.path.exists("data/bad_words.txt"):
        return []

    with open("data/bad_words.txt", "rt") as _f:
        return _f.read().splitlines()
