from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article, Source
from .serializers import ArticleSerializer, SourceSerializer


class SourceList(generics.ListAPIView):
    """Active feeds, so n8n reads its feed list from Django instead of hardcoding it."""
    queryset = Source.objects.filter(is_active=True)
    serializer_class = SourceSerializer
    pagination_class = None


class ArticleCreate(generics.CreateAPIView):
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        existing = Article.objects.filter(url=request.data.get('url')).first()
        if existing:
            return Response(ArticleSerializer(existing).data | {'duplicate': True}, status=status.HTTP_200_OK)
        response = super().create(request, *args, **kwargs)
        response.data['duplicate'] = False
        return response


class ArticleUpdate(generics.RetrieveUpdateAPIView):
    """Lets a separate workflow add the Turkmen translation later."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@api_view(['POST'])
def check_urls(request):
    """Body: {"urls": [...]}. Returns the URLs not yet stored, so n8n skips the AI step for known articles."""
    urls = request.data.get('urls') or []
    if not isinstance(urls, list):
        return Response({'error': '"urls" must be a list'}, status=status.HTTP_400_BAD_REQUEST)
    known = set(Article.objects.filter(url__in=urls).values_list('url', flat=True))
    return Response({'new': [u for u in urls if u not in known]})
