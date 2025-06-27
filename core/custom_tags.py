from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key, [])

@register.filter
def slugify(value):
    return slugify(value)


from django import template
register = template.Library()

@register.filter
def dict_status_count(comments, status_name):
    return len([c for c in comments if getattr(c.candidate, 'follow_up_status', '') == status_name])
