from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from blog.sitemap import *

admin.autodiscover()

urlpatterns = patterns('',

    # administration
    (r'^admin/', include(admin.site.urls)),

    # allow robots
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: Twitterbot\nDisallow: \n\nUser-agent: *\nDisallow: /tag\nDisallow: /chrono\nDisallow: /static\n\nSitemap: http://carabana.cz/sitemap.xml", mimetype="text/plain")),

    # add sitemap
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # carabana blog
    (r'^', include('blog.urls')),
)


