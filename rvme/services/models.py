from rvme.core.models import TimeStampedFieldsModel
from .surecam.models import Event, Trip


class EventSummary(Event):
    class Meta:
        proxy = True
        verbose_name = 'event summary'
        verbose_name_plural = 'event summaries'


class TripSummary(Trip):
    class Meta:
        proxy = True
        verbose_name = 'trip summary'
        verbose_name_plural = 'trip summaries'
