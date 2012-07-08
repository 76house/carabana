# coding: utf-8

from django.contrib.syndication.views import Feed
from blog.models import Article

class LatestArticlesFeed(Feed):
    title = "čarabaňa.cz"
    description = "Nejnovější články"
    author_name = "Martin Marek"
    link = "/feeds/"
    description_template = 'feeds/articles_description.html'
        
    def items(self):
        return Article.public.all()[:10]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description    

