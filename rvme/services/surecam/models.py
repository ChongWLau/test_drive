from django.conf import settings
from django.db import models

from rvme.bookings.models import Car, Booking, Key
from rvme.core.models import TimeStampedFieldsModel
from .constants import EVENT_TYPES


class IdentityMixin(models.Model):
    device = models.ForeignKey(
        "Device",
        related_name='%(class)ss',
    )
    car = models.ForeignKey(
        "bookings.Car",
        related_name='%(class)ss',
    )
    booking = models.ForeignKey(
        "bookings.Booking",
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
    )
    key = models.ForeignKey(
        "bookings.Key",
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
    )

    class Meta:
        abstract = True


class Device(TimeStampedFieldsModel):
    serial = models.CharField(
        primary_key=True,
        max_length=50,
        editable=False,
    )
    project_id = models.CharField(
        max_length=50
    )
    license_plate = models.CharField(
        max_length=50
    )
    zone = models.CharField(
        max_length=50
    )
    car = models.ForeignKey(
        Car,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['serial']

    def __str__(self):
        return self.serial


class Event(IdentityMixin, TimeStampedFieldsModel):
    event_id = models.CharField(
        primary_key=True,
        max_length=100,
        editable=False,
    )
    timestamp = models.DateTimeField()
    type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    def __str__(self):
        return self.event_id

    class Meta:
        ordering = ['-timestamp']


class Trip(IdentityMixin, TimeStampedFieldsModel):
    trip_id = models.CharField(
        primary_key=True,
        max_length=100,
        editable=False,
    )
    parent_trip = models.ForeignKey(
        "self",
        null=True,
        related_name='child_trips',
    )
    start = models.DateTimeField()
    stop = models.DateTimeField()
    mileage = models.IntegerField(
        help_text="Stored in METRES as that's what the API provides",
    )
    state = models.CharField(
        max_length=100
    )

    class Meta:
        ordering = ['-start']

    def __str__(self):
        return self.trip_id

    @property
    def timestamp(self):
        return self.start
