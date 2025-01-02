from django.contrib import admin
from datetime import datetime
from blog.models import *

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PictureInline(admin.TabularInline):
    model = Picture

class ArticleAdmin(admin.ModelAdmin):
    inlines = [PictureInline,]
    exclude = ['date_modified', 'year_published', 'drawing']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = ['id', 'title', 'status', 'date_modified', 'tag_list']
    ordering = ['-date_modified']

    def save_model(self, request, obj, form, change):

        # set date_published when changing status from DRAFT to PUBLIC
        # note: it is not possible to go from DRAFT to HIDDEN
        if change: 
            old = Article.objects.get(pk = obj.id)
            if old.status == Article.ARTICLE_STATUS_DRAFT:
                if obj.status == Article.ARTICLE_STATUS_PUBLIC:
                    obj.date_published = datetime.now()
                elif obj.status == Article.ARTICLE_STATUS_HIDDEN:
                    obj.status = Article.ARTICLE_STATUS_DRAFT

        obj.year_published = obj.date_published.year
        obj.date_modified = datetime.now()
        super(ArticleAdmin, self).save_model(request, obj, form, change)

class PictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'thumbnail', 'url', 'size', 'dimensions', 'article']


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Picture, PictureAdmin)

