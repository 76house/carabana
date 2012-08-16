from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()

urlpatterns = patterns('',

    # administration
    (r'^admin/', include(admin.site.urls)),

    # allow robots
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /tag\nDisallow: /chrono", mimetype="text/plain")),

    # carabana blog
    (r'^', include('blog.urls')),
)


