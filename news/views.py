from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Article, Category, Source


class ArticleListView(ListView):
    model = Article
    paginate_by = 20
    template_name = 'news/article_list.html'

    def get_queryset(self):
        qs = Article.objects.select_related('source', 'category')
        params = self.request.GET
        if category := params.get('category'):
            qs = qs.filter(category__slug=category)
        if source := params.get('source'):
            qs = qs.filter(source_id=source) if source.isdigit() else qs.none()
        if q := params.get('q', '').strip():
            qs = qs.filter(
                Q(title__icontains=q) | Q(title_tk__icontains=q)
                | Q(summary_en__icontains=q) | Q(summary_tk__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            categories=Category.objects.all(),
            sources=Source.objects.filter(is_active=True),
            current_category=self.request.GET.get('category', ''),
            current_source=self.request.GET.get('source', ''),
            query=self.request.GET.get('q', '').strip(),
        )
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'

    def get_queryset(self):
        return Article.objects.select_related('source', 'category')
