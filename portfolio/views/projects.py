from django.conf import settings
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from portfolio.models import Project, SiteSettings, Technology
from portfolio.utils import (
    SeoMixin,
    absolute_media_url,
    absolute_url,
    as_datetime,
    item_list_data,
    project_data,
)


class ProjectsView(SeoMixin, ListView):
    template_name = "pages/projects.html"
    model = Project
    context_object_name = "projects"
    paginate_by = 9
    seo_page_key = "projects"

    def get_seo_breadcrumbs(self):
        return [("projects", _("Réalisations"))]

    def get_seo_overrides(self):
        projects = list(getattr(self, "object_list", []) or [])
        if not projects:
            projects = list(self.get_queryset()[:50])
        return {
            "structured_data": [
                item_list_data(
                    [
                        {
                            "name": project.title,
                            "url": absolute_url(
                                project.get_absolute_url(), self.request
                            ),
                        }
                        for project in projects
                    ],
                    request=self.request,
                    name=_("Réalisations"),
                )
            ]
        }

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


class ProjectDetailView(SeoMixin, DetailView):
    template_name = "projects/project_detail.html"
    model = Project
    context_object_name = "project"
    slug_url_kwarg = "slug"
    seo_page_key = "projects"

    def get_seo_breadcrumbs(self):
        return [("projects", _("Réalisations")), (None, self.object.title)]

    def get_seo_overrides(self):
        project = self.object
        return {
            "title": f"{project.title} | {settings.SITE_NAME}",
            "description": project.short_description or project.description,
            "image": absolute_media_url(project.cover_image, self.request),
            "image_alt": project.title,
            "type": "article",
            "publish_time": as_datetime(project.project_date),
            "modify_time": project.updated_at,
            "structured_data": [project_data(project, self.request)],
        }

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

        # Only show media that actually exists on disk (avoids rendering broken
        # image URLs when a file is missing).
        context["gallery_images"] = [
            img
            for img in project.images.all()
            if img.image.name and img.image.storage.exists(img.image.name)
        ]
        context["cover_available"] = bool(
            project.cover_image
            and project.cover_image.name
            and project.cover_image.storage.exists(project.cover_image.name)
        )

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
