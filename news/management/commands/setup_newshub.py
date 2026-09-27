from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from news.models import Category, Source

CATEGORIES = [
    ('world', 'World', 'Dünýä'),
    ('politics', 'Politics', 'Syýasat'),
    ('business', 'Business', 'Ykdysadyýet'),
    ('technology', 'Technology', 'Tehnologiýa'),
    ('science', 'Science', 'Ylym'),
    ('health', 'Health', 'Saglyk'),
    ('sports', 'Sports', 'Sport'),
    ('culture', 'Culture', 'Medeniýet'),
    ('central-asia', 'Central Asia', 'Merkezi Aziýa'),
    ('other', 'Other', 'Beýlekiler'),
]

# Feeds verified to load through the user's proxy on 2026-09-27.
SOURCES = [
    ('BBC World', 'https://feeds.bbci.co.uk/news/world/rss.xml', 'https://www.bbc.com/news/world'),
    ('BBC Technology', 'https://feeds.bbci.co.uk/news/technology/rss.xml', 'https://www.bbc.com/news/technology'),
    ('Al Jazeera', 'https://www.aljazeera.com/xml/rss/all.xml', 'https://www.aljazeera.com'),
    ('DW', 'https://rss.dw.com/rdf/rss-en-all', 'https://www.dw.com/en'),
    ('TechCrunch', 'https://techcrunch.com/feed/', 'https://techcrunch.com'),
    ('Ars Technica', 'https://feeds.arstechnica.com/arstechnica/index', 'https://arstechnica.com'),
    ('The Verge', 'https://www.theverge.com/rss/index.xml', 'https://www.theverge.com'),
    ('Hacker News', 'https://hnrss.org/frontpage', 'https://news.ycombinator.com'),
    ('RFE/RL', 'https://www.rferl.org/api/', 'https://www.rferl.org'),
    ('24.kg', 'https://24.kg/english/rss/', 'https://24.kg/english'),
    ('Gazeta.uz', 'https://www.gazeta.uz/en/rss/', 'https://www.gazeta.uz/en'),
]

API_USERNAME = 'n8n'


class Command(BaseCommand):
    help = 'Create default categories, news sources and the API token n8n uses. Safe to run again.'

    def handle(self, *args, **options):
        for slug, name_en, name_tk in CATEGORIES:
            Category.objects.update_or_create(slug=slug, defaults={'name_en': name_en, 'name_tk': name_tk})
        self.stdout.write(f'Categories: {Category.objects.count()}')

        created = 0
        for name, feed_url, site_url in SOURCES:
            _, was_created = Source.objects.get_or_create(feed_url=feed_url, defaults={'name': name, 'site_url': site_url})
            created += was_created
        self.stdout.write(f'Sources: {Source.objects.count()} ({created} new)')

        user, _ = get_user_model().objects.get_or_create(username=API_USERNAME)
        if user.has_usable_password():
            user.set_unusable_password()
            user.save()
        token, _ = Token.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS(f'API token for n8n: {token.key}'))
