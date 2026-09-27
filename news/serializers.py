from rest_framework import serializers

from .models import Article, Category, Source

FALLBACK_CATEGORY = 'other'


class LenientCategoryField(serializers.SlugRelatedField):
    """Small models sometimes invent category names; file those under 'other'."""

    def to_internal_value(self, data):
        slug = str(data).strip().lower().replace(' ', '-')
        category = Category.objects.filter(slug=slug).first()
        return category or Category.objects.filter(slug=FALLBACK_CATEGORY).first()


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'feed_url', 'site_url']


class ArticleSerializer(serializers.ModelSerializer):
    category = LenientCategoryField(slug_field='slug', queryset=Category.objects.all(), required=False, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=50), required=False)

    class Meta:
        model = Article
        fields = [
            'id', 'url', 'source', 'category', 'title', 'title_tk', 'content',
            'summary_en', 'summary_tk', 'tags', 'image_url', 'published_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
        # Duplicates are handled in the view (returns the existing article), not as an error.
        extra_kwargs = {'url': {'validators': []}}

    def validate_tags(self, value):
        seen = []
        for tag in value:
            tag = tag.strip().lower().lstrip('#')
            if tag and tag not in seen:
                seen.append(tag)
        return seen[:8]
