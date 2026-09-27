from django import template
from django.utils.translation import get_language

from news.ui_text import ui

register = template.Library()


@register.simple_tag
def t(key):
    return ui(key, get_language())


@register.simple_tag(takes_context=True)
def query_with(context, **params):
    """Current query string with some params replaced, for pagination and filter links."""
    query = context['request'].GET.copy()
    for key, value in params.items():
        if value in (None, ''):
            query.pop(key, None)
        else:
            query[key] = value
    if 'page' not in params:
        # Changing a filter should start again from page 1.
        query.pop('page', None)
    encoded = query.urlencode()
    return f'?{encoded}' if encoded else '?'
