from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def metres_to_miles(val):
    return (Decimal(val) / 1000) * Decimal(0.621371)
