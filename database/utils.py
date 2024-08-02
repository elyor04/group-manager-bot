import os


def get_swearing_words():
    if not os.path.exists("data/swearing-words.txt.txt"):
        return []

    with open("data/swearing-words.txt", "rt") as _f:
        return _f.read().splitlines()
