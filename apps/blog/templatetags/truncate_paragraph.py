# coding: utf-8

import re
from django import template

register = template.Library()

@register.filter
def truncate_paragraph(value):
    data = unicode(value)
    data = re.sub('<img (.+)>', '', data)
    data = re.sub('<a (.+)>(?P<link>(.+))</a>', '\g<link>', data)

    i = data.find('</p>')
        
    if i != -1:
        data = data[:(i + 4)]
    
    return data  # .replace("</p>", "&nbsp;&raquo;</p>")

