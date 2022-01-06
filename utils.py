import datetime
import pytz


def get(l, idx, default=""):
    try:
        return l[idx]
    except IndexError:
        return default


def parse_str2datetime(string, time_format="%d/%m/%Y %H:%M:%S", default_timezone=pytz.timezone('Europe/Riga')):
    return datetime.datetime.strptime(string, time_format).replace(tzinfo=default_timezone)
