import re


def extract_username(message_text):
    username_pattern = r"@\w+"
    user_id_pattern = r"\b\d+\b"

    username_match = re.search(username_pattern, message_text)
    username = username_match.group(0) if username_match else None

    user_id_match = re.search(user_id_pattern, message_text)
    user_id = user_id_match.group(0) if user_id_match else None

    return username or user_id
