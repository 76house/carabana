# coding: utf-8

import os
from PIL import Image, ImageEnhance
import PIL.ExifTags
from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import permalink, Manager
from utils import *

# ------------------------------------------------------------------------------
# Tag model
#
class Tag(models.Model):
    name = models.CharField(max_length = 20)
    slug = models.SlugField(max_length = 20, unique = True) # unique URL

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __unicode__(self):
        return "%s" % self.name

    #@permalink
    def get_absolute_url(self):
        return '/tag/%s' % self.slug


# ------------------------------------------------------------------------------
# Picture model
#
class Picture(models.Model):

    PICTURE_ORIGINAL = 0
    PICTURE_SMALL = 300
    PICTURE_BIG = 500

    date_created = models.DateTimeField(default = datetime.now, editable = False)
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to = settings.MEDIA_ROOT + '/picture', height_field = 'height', width_field = 'width')
    width = models.IntegerField(editable = False)
    height = models.IntegerField(editable = False)
    article = models.ForeignKey('blog.Article')

    def __unicode__(self):
        return self.title

    def size(self):
        return self.picture.size

    # picture dimensions for admin
    def dimensions(self):
        return "%s x %s" % (self.width, self.height)

    # return link to picture file with specific size (small, big, original)
    def url(self, width = PICTURE_ORIGINAL):
        src = self.picture.url
        print width
        if width != Picture.PICTURE_ORIGINAL:
            ext = src[-4:].replace('.png', '.jpg').replace('.PNG', '.jpg')
            src = "%s_%d%s" % (src[:-4], width, ext)
            print src
        return src.replace(settings.MEDIA_ROOT + '/', '')
        
    # picture thumbnail for admin
    def thumbnail(self):
        src = settings.MEDIA_URL + self.url(Picture.PICTURE_SMALL)
        return u'<a href="%s%s"><img style="max-width: 300px; max-height: 300px; " src="%s" /></a>' \
            % (settings.MEDIA_URL, self.url(), src )

    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True

    def save(self):

        if not self.id and not self.picture:
            return

        super(Picture, self).save()

        exif = {}
        static_dir = os.path.join(os.path.dirname(__file__), 'static')

        filename = self.picture.url
        basename, ext = os.path.splitext(filename)
        im = Image.open(filename)

        # rotate img as said by the EXIF orientation info
        exif_raw = None
        if ext.lower() == ".jpg":
            exif_raw = im._getexif()
        if exif_raw:
            for tag, value in exif_raw.items():
                decoded = PIL.ExifTags.TAGS.get(tag, tag)
                exif[decoded] = value

        if 'Orientation' in exif.keys():
            orientation = exif['Orientation']
            if orientation == 1:
                # Nothing
                mirror = im
            elif orientation == 2:
                # Vertical Mirror
                mirror = im.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # Rotation 180°
                mirror = im.transpose(Image.ROTATE_180)
            elif orientation == 4:
                # Horizontal Mirror
                mirror = im.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                # Horizontal Mirror + Rotation 270°
                mirror = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
            elif orientation == 6:
                # Rotation 270°
                mirror = im.transpose(Image.ROTATE_270)
            elif orientation == 7:
                # Vertical Mirror + Rotation 270°
                mirror = im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
            elif orientation == 8:
                # Rotation 90°
                mirror = im.transpose(Image.ROTATE_90)
        else:
            # No EXIF information, the user has to do it
            mirror = im

        # generate following widths: 300px, 500px, 600px, 1000px
        #   JPG - common photos and pictures
        #   PNG - transparent drawing + background (save as JPG)

        ratio = mirror.size[1] / (float)(mirror.size[0])
        widths = [ 300, 500, 600, 1000 ]

        if ext.lower() == '.jpg':
            mirror.save(filename, "JPEG", quality = 95)
        else:
            mirror.save(filename)

        for width in widths:
            thumb = mirror.copy()
            size = (width, int(width * ratio))
            self.width, self.height = size
            filename = '%s_%d%s' % (basename, width, ext)

            thumb = thumb.resize(size, Image.ANTIALIAS)
            sharpener = ImageEnhance.Sharpness(thumb)
            thumb = sharpener.enhance(1.4)

            # use two backgroud variants for transparent PNGs based on picture width (1x up to 500px, 2x above 500px)
            if ext.lower() == '.png':
                filename = '%s_%d%s' % (basename, width, ".jpg")
                if width <= 500:
                    bg = Image.open(static_dir + '/img/bg_1x.jpg')
                else:
                    bg = Image.open(static_dir + '/img/bg_2x.jpg')

                bg.paste(thumb, (0, 0), thumb)
                box = (0, 0, self.width, self.height)
                bg = bg.crop(box)
                bg.save(filename, "JPEG", quality = 90)

            elif ext.lower() == '.jpg':
                thumb.save(filename, "JPEG", quality = 90)
            else:
                thumb.save(filename)

        if self.article:
            self.article.save()
            


# ------------------------------------------------------------------------------
# Custom Manager to provide published articles (ordered descendantly by date_published)
#
class PublicArticleManager(models.Manager):
    def get_query_set(self):
        return super(PublicArticleManager, self).get_query_set().filter(status = Article.ARTICLE_STATUS_PUBLIC).order_by('-date_published')


# ------------------------------------------------------------------------------
# Article model
#
class Article(models.Model):

    # available article statuses
    ARTICLE_STATUS_DRAFT = 1
    ARTICLE_STATUS_PUBLIC = 2
    ARTICLE_STATUS_HIDDEN = 3
    ARTICLE_STATUS_CHOICES = (
        (ARTICLE_STATUS_DRAFT,  'Draft'),
        (ARTICLE_STATUS_PUBLIC, 'Public'),
        (ARTICLE_STATUS_HIDDEN, 'Hidden'),
    )

    title           = models.CharField(max_length = 100, help_text = "Maximum 100 characters")
    slug            = models.SlugField(max_length = 100, unique = True, help_text = "Maximum 100 characters, must be unique") # unique URL
    status          = models.IntegerField(choices = ARTICLE_STATUS_CHOICES, default = ARTICLE_STATUS_DRAFT) # article status
    date_published  = models.DateTimeField(default = datetime.now) # used for showing and sorting
    year_published  = models.IntegerField(default = 0) # hidden, used for grouping
    date_modified   = models.DateTimeField(default = datetime.now) # last modification
    tags            = models.ManyToManyField(Tag, help_text = "Assigned tags") # assigned tags
    perex           = models.TextField(blank = False) # text perex (source)
    body            = models.TextField(blank = False) # text body (source)
    perex_html      = models.TextField(editable = False, blank = True) # text perex (HTML generated from source)
    body_html       = models.TextField(editable = False, blank = True) # text body (HTML generated from source)
    drawing         = models.CharField(max_length = 100) # 'flyer picture' url
    
    # managers to provide all / only published articles
    objects         = models.Manager()
    public          = PublicArticleManager()
 
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-date_published']

    def __unicode__(self):
        return self.title

    # comma-separated tag list
    def tag_list(self):
        return ", ".join([p.name for p in self.tags.all()])
    tag_list.short_description = 'Tags'
    
    # article title for admin (color shows the current status)
    def title_status(self):
        if self.status == Article.ARTICLE_STATUS_DRAFT:
            color = '#f00'
        elif self.status == Article.ARTICLE_STATUS_HIDDEN:
            color = '#999'
        else:
            color = '#090'
        return '<a href="%u"><b><span style="color: %s;">%s</span></b></a>' % (self.id, color, self.title)
    title_status.short_description = 'Title'
    title_status.allow_tags = True

    # URL of assigned drawing image (transparent PNG inserted to perex / body and named 'drawing')
    def drawing_url(self):
        return '%s/%s' % (settings.MEDIA_URL, self.drawing)

    def save(self, force_insert = False, force_update = False, **kwargs):

        # insert URL and CSS style for all inserted pictures in perex / body
        # remember drawing image, if inserted
        for picture in self.picture_set.all():
            if picture.title == "drawing":
                self.drawing = picture.url(Picture.PICTURE_SMALL)
                style = ""
            else:
                style = "[.tilted]"
            picture_tag = "![%s]\r" % picture.title
            tag_replace = "![%s](%s)%s\r" % (picture.title, picture.url(Picture.PICTURE_BIG), style )
            self.perex = self.perex.replace(picture_tag, tag_replace)
            self.body = self.body.replace(picture_tag, tag_replace)

        # convert Markdown-compatible text markup to pure HTML
        self.perex_html = process_markup(self.perex, True)
        self.body_html = process_markup(self.body)
        super(Article, self).save(force_insert, force_update, **kwargs)

    #@permalink
    def get_absolute_url(self):
        return '/blog/%s' % self.slug


