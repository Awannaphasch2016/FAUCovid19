import datetime


def _get_epoch_datetime_subtract_timedelta(timestamp: datetime.datetime,
                                           frequency: str,
                                           interval: int) -> datetime.datetime:
    if frequency == 'day':
        after_timestamp_utc = timestamp - datetime.timedelta(
            days=interval)
    elif frequency == 'hour':
        after_timestamp_utc = timestamp - datetime.timedelta(
            hours=interval)
    elif frequency == 'minute':
        after_timestamp_utc = timestamp - datetime.timedelta(
            minutes=interval)
    elif frequency == 'second':
        after_timestamp_utc = timestamp - datetime.timedelta(
            seconds=interval)
    else:
        raise NotImplementedError
    return after_timestamp_utc


def _convert_timedelta_to_specified_frequency(
        duration: datetime.timedelta,
        frequency: str) -> int:
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if frequency == 'day':
        return days
    elif frequency == 'hour':
        return hours
    elif frequency == 'minute':
        return minutes
    elif frequency == 'second':
        return seconds
    else:
        raise NotImplementedError
