from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Article, Category, Source


class ApiTests(TestCase):
    def setUp(self):
        call_command('setup_newshub', stdout=open('/dev/null', 'w'))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {Token.objects.get().key}')
        self.source = Source.objects.get(name='BBC World')
        self.payload = {
            'url': 'https://example.com/a1',
            'source': self.source.pk,
            'title': 'Something happened',
            'summary_en': 'A short summary.',
            'category': 'world',
            'tags': ['Economy', '#economy', ' trade '],
            'published_at': '2026-09-27T10:00:00Z',
        }

    def test_requires_token(self):
        response = APIClient().post(reverse('news:api-article-create'), self.payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_article(self):
        response = self.client.post(reverse('news:api-article-create'), self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data['duplicate'])
        article = Article.objects.get()
        self.assertEqual(article.category.slug, 'world')
        self.assertEqual(article.tags, ['economy', 'trade'])

    def test_duplicate_returns_existing(self):
        self.client.post(reverse('news:api-article-create'), self.payload, format='json')
        response = self.client.post(reverse('news:api-article-create'), self.payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['duplicate'])
        self.assertEqual(Article.objects.count(), 1)

    def test_unknown_category_falls_back_to_other(self):
        self.payload['category'] = 'Space Exploration'
        self.client.post(reverse('news:api-article-create'), self.payload, format='json')
        self.assertEqual(Article.objects.get().category.slug, 'other')

    def test_add_translation_later(self):
        article_id = self.client.post(reverse('news:api-article-create'), self.payload, format='json').data['id']
        response = self.client.patch(
            reverse('news:api-article-update', args=[article_id]),
            {'title_tk': 'Bir zat boldy', 'summary_tk': 'Gysga mazmun.'}, format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.get().summary_tk, 'Gysga mazmun.')

    def test_check_urls(self):
        self.client.post(reverse('news:api-article-create'), self.payload, format='json')
        response = self.client.post(
            reverse('news:api-check-urls'), {'urls': ['https://example.com/a1', 'https://example.com/new']}, format='json',
        )
        self.assertEqual(response.data['new'], ['https://example.com/new'])

    def test_sources_lists_only_active(self):
        Source.objects.filter(name='DW').update(is_active=False)
        response = self.client.get(reverse('news:api-sources'))
        names = [s['name'] for s in response.data]
        self.assertIn('BBC World', names)
        self.assertNotIn('DW', names)


class SiteTests(TestCase):
    def setUp(self):
        call_command('setup_newshub', stdout=open('/dev/null', 'w'))
        world = Category.objects.get(slug='world')
        tech = Category.objects.get(slug='technology')
        Article.objects.create(url='https://e.com/1', title='Peace talks', title_tk='Parahatçylyk gepleşikleri',
                               summary_en='Talks began.', summary_tk='Gepleşikler başlady.', category=world)
        Article.objects.create(url='https://e.com/2', title='New phone', summary_en='A phone launched.', category=tech)

    def test_english_list(self):
        response = self.client.get(reverse('news:list'))
        self.assertContains(response, 'Peace talks')
        self.assertContains(response, 'Latest news')

    def test_turkmen_list_with_fallback(self):
        response = self.client.get(reverse('news:list'), HTTP_ACCEPT_LANGUAGE='tk')
        self.assertContains(response, 'Parahatçylyk gepleşikleri')
        self.assertContains(response, 'New phone')  # no translation yet, falls back to English
        self.assertContains(response, 'Soňky habarlar')

    def test_category_filter(self):
        response = self.client.get(reverse('news:list'), {'category': 'technology'})
        self.assertContains(response, 'New phone')
        self.assertNotContains(response, 'Peace talks')

    def test_search(self):
        response = self.client.get(reverse('news:list'), {'q': 'gepleşik'})
        self.assertContains(response, 'Peace talks')
        self.assertNotContains(response, 'New phone')

    def test_bad_source_param(self):
        response = self.client.get(reverse('news:list'), {'source': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No news yet.')

    def test_detail_turkmen_pending_notice(self):
        article = Article.objects.get(url='https://e.com/2')
        response = self.client.get(article.get_absolute_url(), HTTP_ACCEPT_LANGUAGE='tk')
        self.assertContains(response, 'Terjime entek taýýar däl')
