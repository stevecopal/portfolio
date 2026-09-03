from django.views.generic import ListView, DetailView
from portfolio.models import Project, Technology, SiteSettings


class ProjectsView(ListView):
    template_name = "pages/projects.html"
    model = Project
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        return (
            Project.objects
            .filter(is_published=True)
            .prefetch_related("technologies", "images")
            .order_by("-project_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        context["technologies"] = Technology.objects.order_by("display_order")
        context["current_tech"] = self.request.GET.get("tech", "")
        return context


class ProjectDetailView(DetailView):
    template_name = "projects/project_detail.html"
    model = Project
    context_object_name = "project"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Project.objects
            .prefetch_related("technologies", "images")
            .filter(is_published=True)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["site_settings"] = SiteSettings.objects.first()

        # Related projects (same technologies)
        context["related_projects"] = (
            Project.objects
            .filter(
                is_published=True,
                technologies__in=project.technologies.all(),
            )
            .exclude(id=project.id)
            .distinct()
            .prefetch_related("technologies", "images")
            .order_by("?")[:3]
        )

        return context


projects_view = ProjectsView.as_view()
project_detail_view = ProjectDetailView.as_view()
