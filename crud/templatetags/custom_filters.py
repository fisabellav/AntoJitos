from django import template

register = template.Library()

@register.filter
def dict_get(value, arg):
    return value.get(arg, '')