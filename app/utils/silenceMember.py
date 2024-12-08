import os
from .config import DATA_DIR


def silence_member(chat_id: int, user_id: int):
    member = (chat_id, user_id)
    members = _get_members()

    if member not in members:
        members.append(member)

        with open(_members_path, "wt") as _f:
            _f.write("\n".join([f"{member[0]},{member[1]}" for member in members]))


def unsilence_member(chat_id: int, user_id: int):
    member = (chat_id, user_id)
    members = _get_members()

    if member in members:
        members.remove(member)

        with open(_members_path, "wt") as _f:
            _f.write("\n".join([f"{member[0]},{member[1]}" for member in members]))


def is_silenced(chat_id: int, user_id: int):
    member = (chat_id, user_id)
    members = _get_members()

    return member in members


def _get_members():
    if not os.path.exists(_members_path):
        return []

    with open(_members_path, "rt") as _f:
        return [tuple(map(int, member.split(","))) for member in _f.read().splitlines()]


_members_path = os.path.join(DATA_DIR, "silenced-members.txt")
