# coding: utf-8

import re
from datetime import datetime
from markdown import markdown
from django.utils.html import escape
from django.conf import settings
from django.utils.safestring import mark_safe

# Convert Markdown markup to pure HTML
# and post-process the code
def process_markup(source, pure_text = False):

    # markdown
    result = markdown(source, extensions=['codehilite', 'markdown.extensions.tables'])

    # -- text post-processing --
    
    # insert non-breaking spaces after some Czech single-letter prepositions
    result = re.sub(r' (?P<letter>[kosuvzKOSUVZ]) ', r' \g<letter>&nbsp;', result)

    # convert [.my_class] to class="my_class"
    result = re.sub(r'>\[\.(?P<class>[a-zA-Z]([ \w-]+))\]', r' class="\g<class>">', result)
    result = re.sub(r' \/ class=', r' class=', result)

    # convert [#my_id] to id="my_id"
    result = re.sub(r'>\[\#(?P<id>[a-zA-Z]([\w-]+))\]', r' id="\g<id>">', result)

    # convert [floatbox]...[/floatbox] to <div class="floatbox"> ... </div>
    result = re.sub(r'\[floatbox\]', r'<div class="floatbox">', result)
    result = re.sub(r'\[\/floatbox\]', r'</div><!--floatbox-->', result)
    
    # convert [download] to <a class="floatbox"> ... </a>
    result = re.sub(r'\[download (?P<href>([^ ]+)) \| (?P<title>([^\]]+))\]', r'<a href="\g<href>" class="download"><span class="btn-download"></span> \g<title></a>', result)
    
    # adjust image source (img in /static directory, picture in  /media directory)
    result = re.sub(r'src="img/', r'src="' + settings.STATIC_URL + 'img/', result)
    result = re.sub(r'src="picture/', r'src="' + settings.MEDIA_URL + 'picture/', result)
    result = re.sub(r'<p><img (?P<img>(.+))></p>', r'<img \g<img>>', result)
    result = re.sub(r' alt="drawing" ', r' class="drawing" ', result)
    result = re.sub(r' alt="nosize" ', r' class="nosize" ', result)

    # embed [flickr] object
    result = re.sub(r'<p>\[flickr (?P<id>([\w\/]+)) \| (?P<src>([^ ]+)) \| (?P<title>([^\]]+))\]<\/p>',
        r'<a href="https://www.flickr.com/photos/\g<id>/" title="\g<title>"><img class="tilted" src="\g<src>" alt="\g<title>"></a>', result)

    # embed [youtube] object
    result = re.sub(r'<p>\[youtube (?P<id>([\w_-]+))\]<\/p>',
        r'<iframe class="youtube" src="https://www.youtube.com/embed/\g<id>?rel=0" allowfullscreen></iframe>', result)

    # embed [slideshare] object
    result = re.sub(r'<p>\[slideshare (?P<id>([\w]+))\]<\/p>',
        r'<iframe class="document" src="http://www.slideshare.net/slideshow/embed_code/\g<id>?rel=0" scrolling="no" allowfullscreen></iframe>', result)

    # embed [sliderocket] object
    result = re.sub(r'<p>\[sliderocket (?P<id>([\w\-]+))\]<\/p>',
        r'<iframe class="document" src="http://app.sliderocket.com:80/app/fullplayer.aspx?id=\g<id>" scrolling="no" allowfullscreen></iframe>', result)

    result = mark_safe(result)
    return result

