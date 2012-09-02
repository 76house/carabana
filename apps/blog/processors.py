from datetime import datetime
from django.conf import settings
from django.core.cache import cache

import twitter
import flickrapi


# get latest tweets from preconfigured twitter account (cached)
def latest_tweets(request):
    tweets = cache.get('tweets')

    if settings.DEBUG:
      return { "tweets" : () } # disable this time-consuming functionality (useful for testing)

    if tweets:
        return {"tweets": tweets}

    # lazy fetch via twitter API
    tweets = twitter.Api().GetUserTimeline(settings.TWITTER_USER)[:settings.TWITTER_ITEMCOUNT]
    for t in tweets:
        t.date = datetime.strptime(t.created_at, "%a %b %d %H:%M:%S +0000 %Y")

    cache.set('tweets', tweets, settings.TWITTER_TIMEOUT)

    return {"tweets": tweets}


# get latest public photos from preconfigured flickr account (cached)
def latest_photos(request):
    photos = cache.get('photos')

    if settings.DEBUG:
      return { "photos" : () } # disable this time-consuming functionality (useful for testing)

    if photos:
        return {"photos": photos}

    # lazy fetch via flicker API
    photos = []
    flickr = flickrapi.FlickrAPI(settings.FLICKR_KEY)
    photowalk = flickr.walk(user_id = settings.FLICKR_USER, per_page = settings.FLICKR_ITEMCOUNT)
    
    for i in range(settings.FLICKR_ITEMCOUNT):
        photo = photowalk.next()
        if photo is not None:
            id = photo.attrib['id']
            secret = photo.attrib['secret']
            server_id = photo.attrib['server']
            farm_id = photo.attrib['farm']
            user_id = photo.attrib['owner']
            title = photo.attrib['title']

            # calculate the thumbnail URL and photo URL
            # http://www.flickr.com/services/api/misc.urls.html
            thumbnail_url = "http://farm%s.static.flickr.com/%s/%s_%s_q.jpg" % (farm_id, server_id, id, secret)
            photo_url = "http://www.flickr.com/photos/%s/%s"  % (user_id, id)
            t = thumbnail_url, photo_url, title
            photos.append(t)

    cache.set('photos', photos, settings.FLICKR_TIMEOUT)

    return {"photos": photos}

