from django.conf import settings
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from portfolio.models import Project, Service, SiteSettings
from portfolio.utils import (
    SeoMixin,
    absolute_media_url,
    absolute_url,
    item_list_data,
    service_data,
)


class ServicesView(SeoMixin, ListView):
    template_name = "pages/services.html"
    model = Service
    context_object_name = "services"
    queryset = Service.objects.filter(is_active=True).order_by("display_order")
    seo_page_key = "services"

    def get_seo_breadcrumbs(self):
        return [("services", _("Solutions"))]

    def get_seo_overrides(self):
        services = list(self.get_queryset())
        return {
            "include_service_catalog": True,
            "structured_data": [
                item_list_data(
                    [
                        {
                            "name": service.title,
                            "url": absolute_url(
                                service.get_absolute_url(), self.request
                            ),
                        }
                        for service in services
                    ],
                    request=self.request,
                    name=_("Solutions"),
                )
            ],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        return context


services_view = ServicesView.as_view()


class ServiceDetailView(SeoMixin, DetailView):
    template_name = "services/service_detail.html"
    model = Service
    context_object_name = "service"
    slug_url_kwarg = "slug"
    seo_page_key = "services"

    def get_seo_breadcrumbs(self):
        return [("services", _("Solutions")), (None, self.object.title)]

    def get_seo_overrides(self):
        service = self.object
        return {
            "title": f"{service.title} | {settings.SITE_NAME}",
            "description": service.hero_description or service.short_description,
            "image": absolute_media_url(service.image, self.request),
            "image_alt": service.title,
            "type": "article",
            "modify_time": service.updated_at,
            "structured_data": [
                service_data(service, self.request),
                item_list_data(
                    [
                        {
                            "name": other.title,
                            "url": absolute_url(
                                other.get_absolute_url(), self.request
                            ),
                        }
                        for other in Service.objects.filter(is_active=True)
                        .exclude(id=service.id)
                        .order_by("display_order")
                    ],
                    request=self.request,
                    name=_("Autres solutions"),
                ),
            ],
        }

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
