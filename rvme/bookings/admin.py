from django.contrib import admin
from django.contrib.admin import register
from django.forms import BaseInlineFormSet
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import localize
from django.utils.safestring import mark_safe

from .models import Booking, Car, Location, Key, KeyHistory, CarClass, CarModel


class KeyHistoryInlineAdmin(admin.TabularInline):
    extra = 0
    fields = [
        'operation', 'status', 'created'
    ]
    model = KeyHistory
    readonly_fields = [
        'operation', 'status', 'created',
       ]


class KeyInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super(KeyInlineFormSet, self).get_queryset()
        return qs[:20]


class KeyInlineAdmin(admin.TabularInline):
    extra = 0
    # exclude = ['user', ]
    fields = readonly_fields = [
        'user', 'keycore_id', 'booking', 'is_put_back', 'is_deleted', 'history_display',
        'created', 'modified',
    ]
    formset = KeyInlineFormSet
    model = Key

    def history_display(self, instance):
        output = []
        for kh in instance.history.all():
            output.append("<strong>{}</strong>: {}, {}".format(
                localize(timezone.localtime(kh.created)),
                kh.get_operation_display(), kh.get_status_display()
            ))
        return mark_safe("<br>".join(output))

    history_display.short_description = "history"


@register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = [KeyInlineAdmin, ]
    list_display = [
        'user', 'id_display', 'location_display', 'car', 'start_time', 'end_time',
        'created', 'modified',
    ]
    list_filter = [
        'user', 'start_time', 'car', 'start_location',
    ]
    save_on_top = True
    search_fields = [
        'user__email',
    ]

    class Media:
        css = {
            'all': ('css/admin.css',),
        }

    def get_changeform_initial_data(self, request):
        return {"completed_on": timezone.now()}

    def id_display(self, obj):
        return obj.id

    id_display.short_description = "booking ID"

    def location_display(self, obj):
        end_location_name = obj.end_location.name if obj.end_location else "Unknown"
        return "{} -> {}".format(
            obj.start_location.name, end_location_name
        )

    location_display.short_description = "location"


@register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'registration_number', 'model', 'address', 'created', 'modified'
    ]
    list_filter = [
        'model__make', 'model__name', 'location',
    ]

    def address(self, obj):
        address = str(obj.location).replace(", ", ",<br>")
        return address

    address.allow_tags = True
    address.short_description = "current location"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['location', ]
        return []


@register(CarClass)
class CarClassAdmin(admin.ModelAdmin):
    list_display = [
        'label', 'created', 'modified',
    ]


@register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'car_class', 'year', 'engine', 'current_type', 'created', 'modified'
    ]


@register(Key)
class KeyAdmin(admin.ModelAdmin):
    inlines = [
        KeyHistoryInlineAdmin,
    ]
    list_display = [
        'keycore_id', 'user', 'get_booking', 'get_booking_start', 'get_booking_end',
        'latest_operation', 'latest_status', 'is_put_back',
        'is_deleted', 'created', 'modified'
    ]
    list_filter = [
        'user', 'latest_operation', 'latest_status', 'is_put_back', 'is_deleted',
    ]
    readonly_fields = [
        'user', 'booking', 'is_put_back', 'is_deleted', 'created',
    ]

    class Media:
        css = {
            'all': ('css/admin.css',),
        }

    def get_booking(self, instance):
        return '<a href="{}">Booking {}</a>'.format(
            reverse(
                "admin:bookings_booking_change", args=(instance.booking.pk,)
            ),
            instance.booking.pk,
        )

    get_booking.allow_tags = True
    get_booking.short_description = "booking"

    def get_booking_start(self, obj):
        return obj.booking.start_time

    get_booking_start.short_description = "booking start"

    def get_booking_end(self, obj):
        return obj.booking.end_time

    get_booking_end.short_description = "booking end"


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'address', 'city', 'county', 'postcode', 'created', 'modified'
    ]
