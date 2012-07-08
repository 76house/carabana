"""

Simple tests for the blog application
Run: "manage.py test"


"""
from django.test import TestCase
from blog.models import *


class BlogTests(TestCase):

    fixtures = ['testdata.json']

    def setUp(self):
        self.tag1 = Tag.objects.create(name="tag1", slug="tag1")
        self.article1 = Article.objects.create(title="Testovaci clanek", slug="testovaci-clanek", status = Article.ARTICLE_STATUS_PUBLIC)
        self.article1.tags.add(self.tag1)
        
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        response = self.client.get('/index.html')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/blog')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/chrono')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/view_chrono.html')

        response = self.client.get('/tag')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/view_tag.html')

        response = self.client.get('/tag/tag1') # from tag1 object
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/view_tag.html')

        response = self.client.get('/tag/art') # from testdata.json
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/view_tag.html')

        response = self.client.get('/tag/tag999') # tag does not exist
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/view_tag.html')

        response = self.client.get('/blog/testovaci-clanek')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/view_article.html')

        response = self.client.get('/blog/clanek-3')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/view_article.html')


