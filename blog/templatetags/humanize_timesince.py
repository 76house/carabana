# coding: utf-8

import datetime

from django import template

register = template.Library()

@register.filter(name='timesince_human')
def humanize_timesince(date):
    delta = datetime.datetime.now() - date

    num_years = delta.days / 365
    if (num_years > 1):
        return u"před %d roky" % num_years
    elif (num_years == 1):
        return u"před rokem"

    num_weeks = delta.days / 7
    if (num_weeks > 1):
        return u"před %d týdny" % num_weeks
    elif (num_weeks == 1):
        return u"před týdnem"

    if (delta.days > 1):
        return u"před %d dny" % delta.days
    elif (delta.days == 1 or datetime.datetime.now().day != date.day):
        return u"včera"

    num_hours = delta.seconds / 3600
    if (num_hours > 1):
        return u"před %d hodinami" % num_hours
    elif (num_hours == 1):
        return u"před hodinou"

    num_minutes = delta.seconds / 60
    if (num_minutes > 1):
        return u"před %d minutami" % num_minutes
    elif (num_minutes == 1):
        return u"před minutou"

    return u"před chvilkou"

