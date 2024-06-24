from django import template
from django.conf import settings as django_settings_conf

register = template.Library()


@register.simple_tag
def dj_settings(name: str) -> dict:
    return getattr(django_settings_conf, name.upper())
