# coding: utf-8

import re
from datetime import datetime
from markdown import markdown
from django.utils.html import escape
from django.conf import settings

# Convert Markdown markup to pure HTML
# and post-process the code
def process_markup(source, pure_text = False):

    # markdown
    result = markdown(source, ['codehilite'])

    # -- text post-processing --
    
    # insert non-breaking spaces after some Czech single-letter prepositions
    result = re.sub(' (?P<letter>[kosuvzKOSUVZ]) ', ' \g<letter>&nbsp;', result)

    # convert [.my_class] to class="my_class"
    result = re.sub('>\[\.(?P<class>[a-zA-Z]([ \w-]+))\]', ' class="\g<class>">', result)
    result = re.sub(' \/ class=', ' class=', result)

    # convert [#my_id] to id="my_id"
    result = re.sub('>\[\#(?P<id>[a-zA-Z]([\w-]+))\]', ' id="\g<id>">', result)

    # convert [floatbox]...[/floatbox] to <div class="floatbox"> ... </div>
    result = re.sub('\[floatbox\]', '<div class="floatbox">', result)
    result = re.sub('\[\/floatbox\]', '</div><!--floatbox-->', result)
    
    # convert [download] to <a class="floatbox"> ... </a>
    result = re.sub('\[download (?P<href>([^ ]+)) \| (?P<title>([^\]]+))\]', '<a href="\g<href>" class="download"><span class="btn-download"></span> \g<title></a>', result)
    
    # convert [share] to <div class="share"> ... </div>
    result = re.sub('\[share\]',
        '<div class="share">\
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="https://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>\
<div><a href="https://twitter.com/share" class="twitter-share-button" data-via="76house" <a href="https://twitter.com/share" class="twitter-share-button" data-via="76house" data-size="large">Tweet</a></div>\
</div>\
', result)

    # adjust image source (img in /static directory, picture in  /media directory)
    result = re.sub('src="img/', 'src="' + settings.STATIC_URL + 'img/', result)
    result = re.sub('src="picture/', 'src="' + settings.MEDIA_URL + 'picture/', result)
    result = re.sub('<p><img (?P<img>(.+))></p>', '<img \g<img>>', result)
    result = re.sub(' alt="drawing" ', ' class="drawing" ', result)

    # embed [flickr] object
    result = re.sub('<p>\[flickr (?P<id>([\w\/]+)) \| (?P<src>([^ ]+)) \| (?P<title>([^\]]+))\]<\/p>',
        '<a href="https://www.flickr.com/photos/\g<id>/" title="\g<title>"><img class="tilted" src="\g<src>" alt="\g<title>"></a>', result)

    # embed [youtube] object
    result = re.sub('<p>\[youtube (?P<id>([\w_]+))\]<\/p>',
        '<iframe class="youtube" src="https://www.youtube.com/embed/\g<id>?rel=0" allowfullscreen></iframe>', result)

    # embed [slideshare] object
    result = re.sub('<p>\[slideshare (?P<id>([\w]+))\]<\/p>',
        '<iframe class="document" src="http://www.slideshare.net/slideshow/embed_code/\g<id>?rel=0" scrolling="no" allowfullscreen></iframe>', result)

    # embed [sliderocket] object
    result = re.sub('<p>\[sliderocket (?P<id>([\w\-]+))\]<\/p>',
        '<iframe class="document" src="http://app.sliderocket.com:80/app/fullplayer.aspx?id=\g<id>" scrolling="no" allowfullscreen></iframe>', result)

    return result

