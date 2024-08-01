import re
from datetime import timedelta


def parse_timedelta(time_str):
    matches = re.findall(r"(\d+)([dhm])", time_str)
    if not matches:
        return None

    delta = timedelta()
    for value, unit in matches:
        value = int(value)
        if unit == "d":
            delta += timedelta(days=value)
        elif unit == "h":
            delta += timedelta(hours=value)
        elif unit == "m":
            delta += timedelta(minutes=value)

    return delta


def get_strtime(delta: timedelta):
    str_time = ""

    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    if days:
        str_time += f"{days} days "
    if hours:
        str_time += f"{hours} hours "
    if minutes:
        str_time += f"{minutes} minutes "

    return str_time.strip()
