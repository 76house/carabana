# Create your views here.

from blog.models import Tag, Article
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404  


# home page
def index(request):

    # fetch latest 1 + 4 articles

    try:
        articles = Article.public.all()
        if articles:
            article = articles[0]
        else:
            article = None
        articles = articles[1:5]
    except Article.DoesNotExist:
        articles = None

    return render_to_response('index.html', {
        'article': article,
        'articles': articles
        }, context_instance=RequestContext(request))


# single article + list of similar articles
def view_article(request, slug):   

    # try to get articles with the same tag; optionally get the latest articles with any tags

    article = get_object_or_404(Article, slug = slug, status__in = [ Article.ARTICLE_STATUS_PUBLIC, Article.ARTICLE_STATUS_DRAFT])
    is_draft = False
    if article:
        if article.status == Article.ARTICLE_STATUS_DRAFT:
            is_draft = True
    is_similar = True
    articles = Article.public.filter(tags__in = article.tags.all).exclude(slug = article.slug)
    if not articles or articles.count() < 4:
        is_similar = False
        articles = articles | Article.public.exclude(tags__in = article.tags.all)
    
    return render_to_response('view_article.html', {
        'article': article,
        'is_draft' : is_draft,
        'articles' : articles.distinct('slug')[:4],
        'is_similar' : is_similar,
    }, context_instance=RequestContext(request))


# list articles for given tag; if no tag name is given, list articles for all tags
def view_tag(request, slug = ""):

    tags = {}

    if slug == "":
        tag_list = Tag.objects.all()
    else:
        try:
            tag_list = [ Tag.objects.get(slug = slug) ]
        except:
            tag_list = []

    for tag in tag_list:
        tag_search = [ tag ]
        tags[tag.slug] = (tag, Article.public.filter(tags__in = tag_search))

    if tags == {}:
        raise Http404  

    return render_to_response('view_tag.html', {
        'slug' : slug,
        'tags': sorted(tags.iteritems()),
    }, context_instance=RequestContext(request))


# list articles for given year of publishing; if no year is given, list articles for all years
def view_chrono(request, slug = ""):

    years = {}

    if slug == "":
        year_list = Article.public.order_by('year_published').values_list('year_published', flat = True).distinct()
    else:
        try:
            year_list = [ int(slug) ]
        except:
            year_list = []

    for year in year_list:
        years[year] = Article.public.filter(year_published = year)

    if years == {}:
        raise Http404  

    return render_to_response('view_chrono.html', {
        'slug' : slug,
        'years': sorted(years.iteritems()),
    }, context_instance=RequestContext(request))


