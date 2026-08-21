from django.views.generic import ListView
from django.db.models import Q
from portfolio.models import Project, Article, Service, SiteSettings

class SearchView(ListView):
    template_name = "pages/search.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        if not query:
            return []

        project_results = Project.objects.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query) | Q(description__icontains=query)
        ).filter(is_published=True)

        article_results = Article.objects.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
        ).filter(status="published")

        service_results = Service.objects.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query) | Q(description__icontains=query)
        ).filter(is_active=True)

        return list(project_results) + list(article_results) + list(service_results)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        context["query"] = self.request.GET.get("q", "")
        return context

search_view = SearchView.as_view()