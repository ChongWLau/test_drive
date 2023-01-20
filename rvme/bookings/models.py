from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils import FieldTracker
from model_utils.fields import AutoCreatedField

from rvme.core.models import TimeStampedFieldsModel
from .constants import VEHICLE_MANUFACTURERS, ENGINE_TYPES, KEY_STATUSES, \
    KEY_OPERATIONS, CURRENT_TYPES
from .managers import CarManager


class Booking(TimeStampedFieldsModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="driver",
        related_name="bookings",
    )
    start_location = models.ForeignKey(
        "Location",
        related_name="bookings_starting",
        verbose_name="Pick up location",
    )
    end_location = models.ForeignKey(
        "Location",
        related_name="bookings_ending",
        verbose_name="Drop-off location",
        blank=True,
        null=True,
    )
    start_time = models.DateTimeField(
        db_index=True,
    )
    end_time = models.DateTimeField(
        blank=True,
        help_text="Leave blank to auto-calculate based on the duration.",
        db_index=True,
    )
    car = models.ForeignKey(
        "Car",
        blank=True,
        null=True,
        help_text="You must specify either a car class or a specific car",
    )

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return "{}, {}, {} to {}, {} -> {}".format(
            self.user,
            self.car,
            timezone.localtime(self.start_time),
            timezone.localtime(self.end_time),
            self.start_location.name,
            self.end_location.name if self.end_location else "Unknown",
        )


class Car(TimeStampedFieldsModel):
    registration_number = models.CharField(
        max_length=10
    )
    model = models.ForeignKey(
        "CarModel",
        related_name="cars",
    )
    location = models.ForeignKey(
        "bookings.Location",
        related_name="cars",
        verbose_name="current location",
    )

    objects = CarManager()

    class Meta:
        ordering = ['registration_number']

    def __str__(self):
        return self.registration_number


class CarClass(TimeStampedFieldsModel):
    label = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name_plural = 'car classes'

    def __str__(self):
        return self.label


class CarModel(TimeStampedFieldsModel):
    make = models.CharField(
        max_length=12,
        choices=VEHICLE_MANUFACTURERS,
        default=VEHICLE_MANUFACTURERS.byd,
    )
    name = models.CharField(
        max_length=20,
        default="E6",
    )
    car_class = models.ForeignKey(
        "CarClass",
        related_name="carmodels",
    )
    year = models.PositiveIntegerField(
        default=2018,
    )
    engine = models.CharField(
        "engine / fuel type",
        max_length=8,
        choices=ENGINE_TYPES,
        default=ENGINE_TYPES.electric,
    )
    current_type = models.CharField(
        max_length=2,
        choices=CURRENT_TYPES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(
            self.get_make_display(), self.name
        )


class Key(TimeStampedFieldsModel):
    keycore_id = models.AutoField(
        primary_key=True,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="driver",
    )
    booking = models.ForeignKey(
        "Booking",
        related_name="keys",
    )
    is_put_back = models.BooleanField(
        default=False,
    )
    is_deleted = models.BooleanField(
        default=False,
    )
    latest_operation = models.CharField(
        max_length=7,
        choices=KEY_OPERATIONS,
        editable=False,
    )
    latest_status = models.CharField(
        max_length=9,
        choices=KEY_STATUSES,
        editable=False,
    )

    tracker = FieldTracker()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.pk)


class KeyHistory(models.Model):
    key = models.ForeignKey(
        "Key",
        related_name="history",
    )
    operation = models.CharField(
        max_length=7,
        choices=KEY_OPERATIONS,
    )
    status = models.CharField(
        max_length=9,
        choices=KEY_STATUSES,
    )
    created = AutoCreatedField(_('created'))

    def __str__(self):
        return str(self.pk)


class Location(TimeStampedFieldsModel):
    name = models.CharField(
        max_length=255
    )
    address = models.CharField(
        max_length=255,
    )
    city = models.CharField(
        max_length=255,
        verbose_name="Town / City",
    )
    county = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    postcode = models.CharField(
        max_length=10,
    )
    latitude = models.DecimalField(
        blank=True,
        decimal_places=8,
        max_digits=10,
        null=True,
    )
    longitude = models.DecimalField(
        blank=True,
        decimal_places=8,
        max_digits=10,
        null=True,
    )

    def __str__(self):
        str_fields = [self.name, self.address, self.city]
        if self.county:
            str_fields.append(self.county)
        str_fields.append(self.postcode)
        return ", ".join(str_fields)

