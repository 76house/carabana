from django import template
register = template.Library()

@register.simple_tag
def actual(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'actual'
    return ''
