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
