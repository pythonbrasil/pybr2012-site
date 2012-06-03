from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def is_active(current_path, urls):
    if current_path in (reverse(url) for url in urls.split()):
        return "active"
    return ""
