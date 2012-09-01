from django.utils.safestring import mark_safe
from django import template
register = template.Library()

@register.filter
def tag_list(tags):
    items = []
    if tags:
        for t in tags:
            items.append('<a href="' + t.get_absolute_url() + '" class="squared">#' + t.name + '</a>')
        
    return mark_safe(" ".join(i for i in items))


