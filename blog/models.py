import os
import re
from PIL import Image, ImageEnhance
import PIL.ExifTags
from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Manager
from django.urls import reverse
from django.utils.text import get_valid_filename
from django.utils.html import format_html
from blog.utils import *

# ------------------------------------------------------------------------------
# Tag model
#
class Tag(models.Model):
    name = models.CharField(max_length = 20)
    slug = models.SlugField(max_length = 20, unique = True) # unique URL

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return ("%s" % self.name)

    def get_absolute_url(self):
        return reverse('view_blog_tag', args=[self.slug])


# ------------------------------------------------------------------------------
# Picture model
#
class Picture(models.Model):

    PICTURE_ORIGINAL = 0
    PICTURE_SMALL = 300
    PICTURE_BIG = 600

    date_created = models.DateTimeField(default = datetime.now, editable = False)
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to = 'picture/', height_field = 'height', width_field = 'width')
    width = models.IntegerField(editable = False)
    height = models.IntegerField(editable = False)
    article = models.ForeignKey('blog.Article', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def size(self):
        return self.picture.size

    # picture dimensions for admin
    def dimensions(self):
        return "%s x %s" % (self.width, self.height)

    # return link to picture file with specific size (small, big, original)
    def url(self, width = PICTURE_ORIGINAL):
        src = self.picture.url
        if (width != Picture.PICTURE_ORIGINAL) and (src.lower().endswith('.png') or src.lower().endswith('.jpg')):
            ext = src[-4:].replace('.png', '.jpg').replace('.PNG', '.jpg')
            src = "%s_%d%s" % (src[:-4], width, ext)
        return src.replace(settings.MEDIA_URL, '')
        
    # picture thumbnail for admin
    def thumbnail(self):
        if self.picture:
            return format_html('<a href="%s"><img style="max-width: 300px; max-height: 300px; " src="%s" /></a>' \
                % (self.url(), self.url(Picture.PICTURE_SMALL) ))
        return "No image"

    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True

    def save(self):

        if not self.id and not self.picture:
            return
        if self.picture.url and hasattr(self.picture.url, 'name'):
            self.picture.url = get_valid_filename(self.picture.url)

        super(Picture, self).save()

        exif = {}

        filename = "." + self.picture.url
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

        # generate following widths: 300px, 600px, 1200px
        #   JPG - common photos and pictures
        #   PNG - transparent drawing + background (save as JPG)

        ratio = mirror.size[1] / (float)(mirror.size[0])
        widths = [ 300, 600, 1200 ]

        if ext.lower() == '.jpg':
            mirror.save(filename, "JPEG", quality = 95)
        else:
            mirror.save(filename)

        for width in widths:
            thumb = mirror.copy()
            size = (width, int(width * ratio))
            self.width, self.height = size
            filename = '%s_%d%s' % (basename, width, ext)

            thumb = thumb.resize(size)
            sharpener = ImageEnhance.Sharpness(thumb)
            thumb = sharpener.enhance(1.4)

            # use two backgroud variants for transparent PNGs based on picture width (1x up to 500px, 2x above 500px)
            if ext.lower() == '.png':
                static_dir = os.path.join(os.path.dirname(__file__), 'static')
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
    def get_queryset(self):
        return super().get_queryset().filter(status=Article.ARTICLE_STATUS_PUBLIC).order_by('-date_published')


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
    keywords        = models.CharField(max_length = 100, help_text = "Custom article keywords for better indexing by search machines")
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
    enable_comments = models.BooleanField(default = False, blank = True)
    
    # managers to provide all / only published articles
    objects         = models.Manager()
    public          = PublicArticleManager()
 
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-date_published']

    def __str__(self):
        return self.title

    # comma-separated tag list
    def tag_list(self):
        return ", ".join([p.name for p in self.tags.all()])
    tag_list.short_description = 'Tags'
    
    # tags as a list
    def taglist(self):
        return self.tags.all()


    # URL of assigned drawing image (transparent PNG inserted to perex / body and named 'drawing')
    def drawing_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.drawing)


    def save(self, force_insert = False, force_update = False, **kwargs):

        super(Article, self).save(force_insert, force_update, **kwargs)

        temp_body = self.body

        # insert URL and CSS style for all inserted pictures in perex / body
        # remember drawing image, if inserted
        for picture in self.picture_set.all():
            picture_size = Picture.PICTURE_BIG
            can_be_link = False
            style = ""
            if picture.title == "drawing":
                self.drawing = picture.url(Picture.PICTURE_SMALL)
            elif picture.title.endswith("-nosize"):
                style = "[.nosize]"
                picture_size = Picture.PICTURE_ORIGINAL
            elif picture.title.endswith("-link"):
                picture_size = Picture.PICTURE_ORIGINAL
                can_be_link = True
            else:
                style = "[.tilted]"
            picture_tag = "![%s]\r" % picture.title
            
            tag_replace = "![%s](%s)%s\r" % (picture.title, picture.url(picture_size), style)
            self.perex = self.perex.replace(picture_tag, tag_replace)
            self.body = self.body.replace(picture_tag, tag_replace)
            temp_body = temp_body.replace(picture_tag, tag_replace)

            print(self.body)

            if can_be_link:
                # convert ![image-link http://example.com] to <a href="http://example.com"><img src="image_url"></a>
                to_search = r'!\[%s (?P<link>([^\]]+))\]' % (picture.title)
                to_replace = r'<a href="\g<link>" class="img"><img src="%s" class="nosize"></a>' % (picture.url(picture_size))
                temp_body = re.sub(to_search, to_replace, temp_body)

        # convert Markdown-compatible text markup to pure HTML
        self.perex_html = process_markup(self.perex, True)
        self.body_html = process_markup(temp_body)

        super(Article, self).save(force_insert, force_update, **kwargs)

    def get_absolute_url(self):
        return reverse('view_blog_article', args=[self.slug])


