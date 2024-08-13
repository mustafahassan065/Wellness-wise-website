# my_app/templatetags/custom_filters.py

from django import template
import datetime

register = template.Library()

@register.filter
def is_available(expert_profile, slot):
    return expert_profile.is_available(slot.start_time, slot.end_time)


@register.filter(expects_localtime=True)
def convert_date(value):
    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')