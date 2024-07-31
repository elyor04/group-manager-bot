import re
from datetime import timedelta


def parse_timedelta(time_str):
    time_pattern = re.compile(r"(\d+)([dhm])")
    matches = time_pattern.findall(time_str)

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
