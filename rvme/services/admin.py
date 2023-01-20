from django.contrib import admin
from django.db.models import Count, Q, Sum, F
from django.db.models.functions import ExtractWeek, ExtractHour

from rvme.core.mixins import ReadOnlyAdminMixin
from rvme.services.constants import PERIOD
from .models import TripSummary, EventSummary

import json


class BaseSummaryAdmin(admin.ModelAdmin):
    list_filter = [
        'car', 'user',
    ]

    class Media:
        css = {
            'all': ('css/admin.css',),
        }


@admin.register(EventSummary)
class EventSummaryAdmin(ReadOnlyAdminMixin, BaseSummaryAdmin):
    change_list_template = 'admin/event_summary_change_list.html'
    date_hierarchy = 'timestamp'

    class Media:
        css = {
            'all': ('css/admin.css',),
        }

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        """
        Generate summary tables
        """
        summary = {
            'low_total': Count('type', filter=Q(type__exact='low')),
            'medium_total': Count('type', filter=Q(type__exact='medium')),
            'high_total': Count('type', filter=Q(type__exact='high')),
            'overspeed_total': Count('type', filter=Q(type__exact='overspeed_start')),
            'total_alerts': F('low_total') + F('medium_total') + F('high_total') + F('overspeed_total')
        }

        driver_summary_qs = qs.exclude(user=None).distinct('user__id', 'user__email').annotate(**summary)

        # TODO #1a: Annotate driver_summary_qs to produce the per-driver event summaries
        # TODO #1a: Output: <QuerySet [
        #  {'user__id': 52, 'user__email': 'testdrive@evezy.co.uk', 'low_total': 451, 'medium_total': 92, 'high_total': 11, 'overspeed_total': 0, 'total_alerts': 554}
        #  ]>
        driver_event_summary = driver_summary_qs
        
        response.context_data['driver_event_summary'] = driver_event_summary

        # TODO #1b: Re-using the filters you wrote above, produce a dictionary containing the totals for all drivers
        # TODO #1b: Output: {'high_total': 11,
        #  'low_total': 451,
        #  'medium_total': 92,
        #  'overspeed_total': 0,
        #  'total_alerts': 554}
        
        driver_event_summary_total = qs.exclude(user=None).annotate(**summary).values(
            'low_total','medium_total','high_total','overspeed_total','total_alerts'
        )

        response.context_data['driver_event_summary_total'] = driver_event_summary_total

        return response


@admin.register(TripSummary)
class TripSummaryAdmin(ReadOnlyAdminMixin, BaseSummaryAdmin):
    change_list_template = 'admin/trip_summary_change_list.html'
    date_hierarchy = 'stop'

    class Media:
        css = {
            'all': ('css/admin.css',),
        }

    def changelist_view(self, request, extra_context=None):

        def generate_by_time_period(qs, period, starting_index):
            """
            Generates an aggregated time-based summary of the Trip queryset passed in. For example, if
            you pass in a period of "week", it will sum up the total_mileage over each day of the week
            for the queryset given.

            :param qs: Queryset of Trip objects
            :param period: hour, week_day or day
            :param starting_index:
            :return:

            When period='week':

            [{'time_period': 1, 'total_mileage': 34},
             {'time_period': 2, 'total_mileage': 96},
             {'time_period': 3, 'total_mileage': 124},
             {'time_period': 4, 'total_mileage': 131},
             {'time_period': 5, 'total_mileage': 199},
             {'time_period': 6, 'total_mileage': 216},
             {'time_period': 7, 'total_mileage': 41}]
            """
            period_lower = period.lower()
            
            if not period_lower in PERIOD:
                raise ("some reasonable 4XX their side / 5XX our side error")

            summary_over_time_period = list(
                qs.filter(
                    # Graph is time-based so we want to ignore parent Trips
                    child_trips__isnull=True
                ).annotate(
                    week=ExtractWeek('timestamp')
                ).annotate(
                    hour=ExtractHour('timestamp')
                ).distinct(
                    period_lower
                ).annotate(
                    time_period=F(period_lower)
                ).annotate(
                    total_mileage=Sum('mileage')
                ).values(
                    'time_period','total_mileage'
                )
                # TODO #3: Complete the rest of this filter to produce the output
                #  above where param period="week"
            )

            """
            This next block will take the data above and normalise it so that for the time period
            given, every possible slot has a value - filling in zeros where necessary - so it
            can be used in the graph on the Trip Summaries page.
            """

            # TODO #4: Remove the line below and modify the array from above so
            #  that the output where param period="hour" looks correct
            
            summary_over_time_period_output = summary_over_time_period

            return summary_over_time_period_output

        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        """
        Generate summary tables
        """

        # TODO #2a: Group the trips by car and count the total number of trips and total mileage.
        #  Output: [{'car__pk': 44,
        #   'car__registration_number': 'PK68 RHW',
        #   'total': 76,
        #   'total_mileage': 635},
        #  {'car__pk': 36,
        #   'car__registration_number': 'BJ68 NDS',
        #   'total': 32,
        #   'total_mileage': 155},
        #  {'car__pk': 55,
        #   'car__registration_number': 'LL68 MTI',
        #   'total': 4,
        #   'total_mileage': 55}]

        summary = {
            'total': Count('trip_id'),
            'total_mileage': Sum('mileage')
        }
        
        car_summary_output = qs.distinct(
            'car__pk','car__registration'
        ).annotate(**summary).values(
            'car__pk','car__registration','total','total_mileage'
        )

        response.context_data['car_summary'] = car_summary_output
        response.context_data['car_summary_json'] = json.dumps(car_summary_output)

        # TODO #2b: Re-using the filters you wrote above, do the same but driver-focused instead of car-focused
        #  Output: [{'total': 112,
        #   'total_mileage': 847,
        #   'user__email': 'testdrive@evezy.co.uk',
        #   'user__id': 52,
        #   'user__pk': 52}]
        
        driver_summary_output = qs.distinct(
            'user__id','user__pk'
        ).annotate(**summary).values(
            'total','total_mileage', 'user__email', 'user__id', 'user__pk'
        )

        response.context_data['driver_summary'] = driver_summary_output
        response.context_data['driver_summary_json'] = json.dumps(driver_summary_output)

        # TODO #2c: Re-using the filters you wrote above, create a dict for the total trips and mileage
        #  Output: {'total': 112, 'total_mileage': 847}
        
        trip_summary_total = driver_summary_output = qs.annotate(**summary).values(
            'total','total_mileage'
        )

        response.context_data['car_summary_total'] = response.context_data['driver_summary_total'] = trip_summary_total

        """
        Generate statistics by hour
        """

        # summary_by_hour = generate_by_time_period(qs, 'hour', starting_index=0)

        # response.context_data['summary_by_hour'] = summary_by_hour
        # response.context_data['summary_by_hour_json'] = json.dumps(
        #     summary_by_hour,
        #     sort_keys=False,
        #     indent=1,
        #     cls=DjangoJSONEncoder
        # )

        """
        Generate statistics by weekday
        """

        # summary_by_weekday = generate_by_time_period(qs, 'week_day', starting_index=1)

        # response.context_data['summary_by_weekday'] = summary_by_weekday
        # response.context_data['summary_by_weekday_json'] = json.dumps(
        #     summary_by_weekday,
        #     sort_keys=False,
        #     indent=1,
        #     cls=DjangoJSONEncoder
        # )

        return response
