from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from portfolio.models import Profile, SiteSettings, Tool
from portfolio.utils import SeoMixin, profile_page_data


class AboutView(SeoMixin, TemplateView):
    template_name = "pages/about.html"
    seo_page_key = "about"

    def get_seo_breadcrumbs(self):
        return [("about", _("À propos"))]

    def get_seo_overrides(self):
        return {"structured_data": [profile_page_data(self.request)]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["site_settings"] = SiteSettings.objects.first()
        context["tools"] = Tool.objects.filter(is_active=True).order_by(
            "display_order", "name"
        )
        return context


about_view = AboutView.as_view()
