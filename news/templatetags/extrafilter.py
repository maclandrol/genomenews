from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    """This is a custom template tag used to reformat the humanize|naturaltime
    this is adapted from a post on stackoverflow about timesince
    http://stackoverflow.com/questions/6481788/format-of-timesince-filter
    """
    return value.split(delimiter)[0]
upto.is_safe = True
