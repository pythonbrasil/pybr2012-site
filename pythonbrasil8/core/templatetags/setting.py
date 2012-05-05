# coding: utf8

from django.conf import settings
from django import template

register = template.Library()


class SettingNode(template.Node):
    def __init__(self, name, asvar):
        self.name = name

        self.asvar = asvar

    def render(self, context):
        if self.asvar:
            context[self.asvar] = getattr(settings, self.name)
            return ''

        else:
            return getattr(settings, self.name)


@register.tag
def setting(parser, token):
    bits = token.split_contents()
    viewname = bits[1]
    asvar = None
    if (viewname.startswith('"') and viewname.endswith('"')) or (viewname.startswith('\'') and viewname.endswith('\'')):
        viewname = viewname[1:-1]

    if len(bits) == 4:
        if bits[2] == 'as':
            asvar = bits[3]
        else:
            raise template.TemplateSyntaxError("usage: {% setting FOO as foo %} or {% setting FOO %}")
    elif len(bits) not in (2, 4):
        raise template.TemplateSyntaxError("usage: {% setting FOO as foo %} or {% setting FOO %}")
    return SettingNode(viewname, asvar)
