from django.contrib.sitemaps import Sitemap
from blog.models import Article

# Sitemap contains all blog articles
class BlogSitemap(Sitemap):
 
    def location(self, obj):
        return obj.get_absolute_url()
 
    def lastmod(self, obj):
        return obj.date_modified or obj.date_published
 
    def items(self):
        return Article.public.all()

# to be fetched in urls.py
sitemaps = dict(blog = BlogSitemap)

