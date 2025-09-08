from django import template
from apps.core.decorators import _is_enabled

register = template.Library()

@register.simple_tag(takes_context=True)
def plugin_enabled(context, code):
    request = context.get("request")
    return _is_enabled(request, code) if request else False