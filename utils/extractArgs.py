import re
from datetime import timedelta
from client import client


async def extract_args(text: str):
    data = {
        "user": None,
        "timedelta": None,
        "reason": None,
    }
    args_text = get_args(text)

    if not args_text:
        return data

    delta = timedelta()

    for arg_text in args_text.split():

        username_match = re.search(r"@\w+", arg_text)
        user_id_match = re.search(r"\b\d{10}\b", args_text)
        timedelta_match = re.findall(r"(\d+)([dhm])", arg_text)

        if username_match:
            username = username_match.group(0)
            chat = await client.get_chat(username)
            chat.full_name = f"{chat.first_name or ''} {chat.last_name or ''}".strip()
            data["user"] = chat

            args_text = args_text.replace(arg_text, "", 1)

        elif user_id_match and (data["chat"] is None):
            user_id = int(user_id_match.group(0))
            chat = await client.get_chat(user_id)
            chat.full_name = f"{chat.first_name or ''} {chat.last_name or ''}".strip()
            data["user"] = chat

            args_text = args_text.replace(arg_text, "", 1)

        elif timedelta_match:
            for value, unit in timedelta_match:
                value = int(value)
                if unit == "d":
                    delta += timedelta(days=value)
                elif unit == "h":
                    delta += timedelta(hours=value)
                elif unit == "m":
                    delta += timedelta(minutes=value)

            args_text = args_text.replace(arg_text, "", 1)

        else:
            data["reason"] = args_text.strip()
            break

    if delta.total_seconds() > 0:
        data["timedelta"] = delta

    return data


def get_args(text: str):
    text_split = text.split(maxsplit=1)
    return text_split[1] if len(text_split) > 1 else None


def get_strtime(delta: timedelta):
    str_time = ""

    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    if days:
        str_time += f"{days} day{'s' if days > 1 else ''} "
    if hours:
        str_time += f"{hours} hour{'s' if hours > 1 else ''} "
    if minutes:
        str_time += f"{minutes} minute{'s' if minutes > 1 else ''} "

    return str_time.strip()
