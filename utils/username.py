import re


def extract_username(message_text):
    username_match = re.search(r"@\w+", message_text)
    username = username_match.group(0)[1:] if username_match else None

    user_id_match = re.search(r"\b\d+\b", message_text)
    user_id = int(user_id_match.group(0)) if user_id_match else None

    return username or user_id
