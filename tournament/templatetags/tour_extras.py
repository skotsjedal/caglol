from django import template
#from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_range(n):
    return range(n)


@register.filter
def get_range_l(dictionary):
    n = int(dictionary['diff'])
    n = (n-1)*3
    return range(n)


@register.filter
def get_dict_val(dictionary, key):
    return dictionary[key]
