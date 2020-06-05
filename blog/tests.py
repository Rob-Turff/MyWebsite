from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from blog.views import home


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'mainpage/home.html')
