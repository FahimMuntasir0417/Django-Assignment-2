from django import template
from django.utils.timesince import timesince
from django.utils.timezone import now

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        return f"{timesince(value, now())} ago"
    return "N/A"