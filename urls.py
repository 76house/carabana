from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    # administration
    (r'^admin/', include(admin.site.urls)),

    # carabana blog
    (r'^', include('blog.urls')),
)


