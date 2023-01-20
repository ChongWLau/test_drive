from django.contrib import admin
from django.contrib.admin import register
from django.forms import BaseInlineFormSet

from rvme.core.templatetags.global_filters import metres_to_miles
from .models import Device, Event, Trip


class IdentityMixinAdminMixin(object):
    readonly_fields = [
        'device', 'car', 'booking', 'key', 'user',
    ]


class MileageInMilesMixin(object):
    def get_fields(self, *args, **kwargs):
        fields = super(MileageInMilesMixin, self).get_fields(*args, **kwargs)
        if 'mileage' in fields:
            fields.remove('mileage')
        return fields

    def mileage_in_miles(self, obj):
        return '{:.2f} miles'.format(metres_to_miles(obj.mileage or 0), 2)

    mileage_in_miles.short_description = "mileage"


class EventInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super(EventInlineFormSet, self).get_queryset()
        return qs[:20]


class EventInlineAdmin(admin.TabularInline):
    extra = 0
    fields = readonly_fields = ['device', 'car', 'get_booking_display', 'key', 'user', 'type', 'timestamp']
    formset = EventInlineFormSet
    model = Event

    def get_booking_display(self, event):
        if event.booking:
            return event.booking.pk
        return None

    get_booking_display.short_description = 'booking'


@register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'serial', 'license_plate', 'car', 'zone', 'created', 'modified'
    ]
    inlines = [
        EventInlineAdmin
    ]
    readonly_fields = [
        'project_id', 'car', 'license_plate', 'zone',
    ]

    def has_add_permission(self, request, obj=None):
        return False


@register(Event)
class EventAdmin(IdentityMixinAdminMixin, admin.ModelAdmin):
    list_display = [
        'car', 'event_id', 'timestamp', 'type', 'get_booking_id', 'key', 'user'
    ]
    list_filter = [
        'type', 'device', 'car', 'user',
    ]

    def get_booking_id(self, event):
        if event.booking:
            return event.booking.id
        return None

    def get_readonly_fields(self, request, obj=None):
        return ['timestamp', 'type'] + super(EventAdmin, self).get_readonly_fields(request, obj)

    def has_add_permission(self, request, obj=None):
        return False


@register(Trip)
class TripAdmin(IdentityMixinAdminMixin, MileageInMilesMixin, admin.ModelAdmin):
    list_display = [
        'trip_id', 'car', 'user', 'start', 'stop', 'mileage_in_miles', 'state', 'modified', 'created'
    ]
    list_filter = [
        'device', 'car', 'user',
    ]

    def get_readonly_fields(self, request, obj=None):
        return ['trip_id', 'parent_trip'] + \
               super(TripAdmin, self).get_readonly_fields(request, obj) + \
               ['start', 'stop', 'mileage', 'state',]

    def has_add_permission(self, request, obj=None):
        return False
