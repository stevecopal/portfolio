from django.views.generic import ListView, DetailView
from django.db.models import Q
from portfolio.models import Article, Category, Tag, SiteSettings

class BlogView(ListView):
    template_name = "pages/blog.html"
    model = Article
    context_object_name = "articles"
    queryset = Article.objects.filter(status="published").order_by("-published_at")
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get("category")
        tag_slug = self.request.GET.get("tag")
        query = self.request.GET.get("q")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
            )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        context["categories"] = Category.objects.order_by("display_order")
        context["tags"] = Tag.objects.order_by("name")
        context["featured_articles"] = Article.objects.filter(
            status="published", is_featured=True
        ).order_by("-published_at")[:3]
        context["latest_articles"] = Article.objects.filter(
            status="published"
        ).order_by("-published_at")[:3]
        return context

blog_view = BlogView.as_view()


class ArticleDetailView(DetailView):
    template_name = "blog/article_detail.html"
    model = Article
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        context["categories"] = Category.objects.order_by("display_order")
        context["tags"] = Tag.objects.order_by("name")
        context["related_articles"] = Article.objects.filter(
            Q(category=self.object.category) | Q(tags__in=self.object.tags.all())
        ).exclude(id=self.object.id).distinct().order_by("?")[:3]
        return context

article_detail_view = ArticleDetailView.as_view()