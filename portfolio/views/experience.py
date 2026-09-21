from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from portfolio.models import Experience, Profile, SiteSettings
from portfolio.utils import SeoMixin, experiences_data


class ExperienceView(SeoMixin, TemplateView):
    template_name = "pages/experience.html"
    seo_page_key = "experience"

    def get_seo_breadcrumbs(self):
        return [("experience", _("Parcours"))]

    def get_seo_overrides(self):
        experiences = list(
            Experience.objects.filter(is_published=True)
            .prefetch_related("related_projects", "technologies")
            .order_by("-start_date")
        )
        structured_data = []
        organizations = experiences_data(experiences)
        if organizations:
            structured_data.append(organizations)
        return {"structured_data": structured_data}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["site_settings"] = SiteSettings.objects.first()
        context["experiences"] = (
            Experience.objects
            .filter(is_published=True)
            .prefetch_related("related_projects", "technologies")
            .order_by("-start_date")
        )
        return context


experience_view = ExperienceView.as_view()
