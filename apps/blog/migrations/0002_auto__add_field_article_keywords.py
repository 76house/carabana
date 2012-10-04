# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.keywords'
        db.add_column('blog_article', 'keywords',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.keywords'
        db.delete_column('blog_article', 'keywords')


    models = {
        'blog.article': {
            'Meta': {'ordering': "['-date_published']", 'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'drawing': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'perex': ('django.db.models.fields.TextField', [], {}),
            'perex_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year_published': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'blog.picture': {
            'Meta': {'object_name': 'Picture'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Article']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['blog']