from django.views.generic import ListView, DetailView
from portfolio.models import Service, Project, SiteSettings


class ServicesView(ListView):
    template_name = "pages/services.html"
    model = Service
    context_object_name = "services"
    queryset = Service.objects.filter(is_active=True).order_by("display_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        return context


services_view = ServicesView.as_view()


class ServiceDetailView(DetailView):
    template_name = "services/service_detail.html"
    model = Service
    context_object_name = "service"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()

        # Related projects (using this service's projects if any)
        context["related_projects"] = (
            Project.objects
            .filter(is_published=True)
            .order_by("-project_date")[:3]
        )

        # All services for navigation
        context["all_services"] = (
            Service.objects.filter(is_active=True)
            .exclude(id=self.object.id)
            .order_by("display_order")
        )

        return context


service_detail_view = ServiceDetailView.as_view()
