import datetime


def datetime_converter(date: datetime) -> str:
    return date.__str__()


def converter(obj):
    if isinstance(obj, datetime.datetime):
        return datetime_converter(obj)

