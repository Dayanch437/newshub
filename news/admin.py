from django.contrib import admin

from .models import Article, Category, Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'feed_url', 'is_active', 'article_count']
    list_editable = ['is_active']
    search_fields = ['name', 'feed_url']

    @admin.display(description='articles')
    def article_count(self, obj):
        return obj.articles.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name_en', 'name_tk']
    prepopulated_fields = {'slug': ['name_en']}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'category', 'published_at', 'has_tk']
    list_filter = ['source', 'category', 'published_at']
    search_fields = ['title', 'title_tk', 'summary_en', 'summary_tk']
    date_hierarchy = 'published_at'
    readonly_fields = ['created_at']

    @admin.display(boolean=True, description='TK')
    def has_tk(self, obj):
        return bool(obj.summary_tk)
