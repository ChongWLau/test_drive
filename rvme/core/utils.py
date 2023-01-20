from django.utils import timezone


def datespan(start_date, end_date, delta=timezone.timedelta(days=1)):
    current_date = start_date
    while current_date < end_date:
        yield current_date
        current_date += delta


def round_to_next_30min(time):
    return time + (
            (timezone.datetime.min - time.replace(tzinfo=None)) % timezone.timedelta(minutes=30)
    )
