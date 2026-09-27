from django.db import models
from django.urls import reverse
from django.utils.translation import get_language


class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)
    feed_url = models.URLField(max_length=500, unique=True)
    site_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name_en = models.CharField(max_length=100)
    name_tk = models.CharField(max_length=100)

    class Meta:
        ordering = ['name_en']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name_en

    @property
    def name(self):
        return self.name_tk if get_language() == 'tk' else self.name_en


class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    url = models.URLField(max_length=1000, unique=True)
    title = models.CharField(max_length=500)
    title_tk = models.CharField(max_length=500, blank=True)
    content = models.TextField(blank=True, help_text='Original text from the feed.')
    summary_en = models.TextField(blank=True)
    summary_tk = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [models.Index(fields=['-published_at'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', args=[self.pk])

    # Turkmen fields fall back to English until a translation exists.
    @property
    def display_title(self):
        if get_language() == 'tk' and self.title_tk:
            return self.title_tk
        return self.title

    @property
    def display_summary(self):
        if get_language() == 'tk' and self.summary_tk:
            return self.summary_tk
        return self.summary_en
