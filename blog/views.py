from blog.models import Tag, Article
from django.template import RequestContext, Context, loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404


def index(request, template = 'index.html', page_template = 'articles_page.html' ):

    # fetch latest 1 + older articles

    try:
        articles = Article.public.all()
        print (articles)
        if articles:
            article = articles[0]
        else:
            article = None
        articles = articles[1:]
    except Article.DoesNotExist:
        articles = None
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        template = page_template

    return render(request, template, {
        'article': article,
        'articles': articles,
        'page_template': page_template,
        })


# single article + list of similar articles
def view_article(request, slug):   

    # try to get articles with the same tag; optionally get the latest articles with any tags

    article = get_object_or_404(Article, slug = slug, status__in = [ Article.ARTICLE_STATUS_PUBLIC, Article.ARTICLE_STATUS_DRAFT])
    is_draft = False
    if article:
        if article.status == Article.ARTICLE_STATUS_DRAFT:
            is_draft = True
    is_similar = True

    # other articlers: 2 similar + 1 newer + 2 older
    #a_tag = list(Article.public.filter(tags__in = article.tags.all).exclude(slug = article.slug)[:2])
    #if not a_tag or len(a_tag) < 2:
    #    is_similar = False
    
    #a_newer = list(Article.public.filter(date_published__gt = article.date_published).exclude(tags__in = article.tags.all).order_by('date_published')[:1])
    #a_older = list(Article.public.filter(date_published__lt = article.date_published).exclude(tags__in = article.tags.all).order_by('-date_published')[:4])
    articles = [] #a_tag + a_newer + a_older
    
    return render(request, 'view_article.html', {
        'article': article,
        'is_draft' : is_draft,
        'articles' : articles[:4],
        'is_similar' : is_similar,
    })


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

    return render(request, 'view_tag.html', {
        'slug' : slug,
        'tags': tags.items(),
        'taglist': Tag.objects.exclude(slug = slug).order_by('name'),
    })


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

    return render(request, 'view_chrono.html', {
        'slug' : slug,
        'years': sorted(years.iteritems()),
    })


