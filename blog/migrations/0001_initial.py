# Generated by Django 5.1.4 on 2024-12-31 21:17

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Maximum 100 characters', max_length=100)),
                ('slug', models.SlugField(help_text='Maximum 100 characters, must be unique', max_length=100, unique=True)),
                ('keywords', models.CharField(help_text='Custom article keywords for better indexing by search machines', max_length=100)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Public'), (3, 'Hidden')], default=1)),
                ('date_published', models.DateTimeField(default=datetime.datetime.now)),
                ('year_published', models.IntegerField(default=0)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('perex', models.TextField()),
                ('body', models.TextField()),
                ('perex_html', models.TextField(blank=True, editable=False)),
                ('body_html', models.TextField(blank=True, editable=False)),
                ('drawing', models.CharField(max_length=100)),
                ('enable_comments', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-date_published'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('title', models.CharField(max_length=20)),
                ('picture', models.ImageField(height_field='height', upload_to='../media/picture', width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.article')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(help_text='Assigned tags', to='blog.tag'),
        ),
    ]