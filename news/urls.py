from django.urls import path

from . import api, views

app_name = 'news'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('api/sources/', api.SourceList.as_view(), name='api-sources'),
    path('api/articles/', api.ArticleCreate.as_view(), name='api-article-create'),
    path('api/articles/<int:pk>/', api.ArticleUpdate.as_view(), name='api-article-update'),
    path('api/articles/check/', api.check_urls, name='api-check-urls'),
]
