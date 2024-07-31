import re
from datetime import timedelta


def parse_timedelta(time_str):
    pattern = r"(\d+)([mhd])"
    match = re.search(pattern, time_str)

    if not match:
        return None

    value, unit = match.groups()
    value = int(value)

    if unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    else:
        return None
