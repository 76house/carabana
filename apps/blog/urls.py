from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.views import *
from blog.feeds import LatestArticlesFeed

urlpatterns = patterns('',

    url(r'^$', 'blog.views.index'),

    url(r'^tag$', 'blog.views.view_tag', name = 'view_blog_tag'),
    url(r'^tag/(?P<slug>[^\.]+)', 'blog.views.view_tag', name = 'view_blog_tag'),

    url(r'^chrono$', 'blog.views.view_chrono', name = 'view_blog_chrono'),
    url(r'^chrono/(?P<slug>[^\.]+)', 'blog.views.view_chrono', name = 'view_blog_chrono'),

    url(r'^blog/(?P<slug>[^\.]+)', 'blog.views.view_article', name = 'view_blog_article'),

    url(r'^feeds/$', LatestArticlesFeed()),

) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + staticfiles_urlpatterns()


