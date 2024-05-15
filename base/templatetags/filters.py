# filters.py

from django import template

register = template.Library()

@register.filter(name='is_integer')
def is_integer(value):
    return isinstance(value, int)
