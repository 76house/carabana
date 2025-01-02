from django.urls import path

from blog.views import index, view_article, view_tag, view_chrono

urlpatterns = [
    path("", index, name="index"),

    path(r'tag', view_tag, name = 'view_blog_tag'),
    path(r'tag/<slug:slug>/', view_tag, name = 'view_blog_tag'),

    path(r'chrono', view_chrono, name = 'view_blog_chrono'),
    path(r'chrono/<slug:slug>/', view_chrono, name = 'view_blog_chrono'),

    path(r'blog/<slug:slug>/', view_article, name = 'view_blog_article'),
]
