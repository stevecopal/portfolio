from django.views.generic import TemplateView
from portfolio.models import Profile, SiteSettings, Tool


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["site_settings"] = SiteSettings.objects.first()
        context["tools"] = Tool.objects.filter(is_active=True).order_by(
            "display_order", "name"
        )
        return context


about_view = AboutView.as_view()
