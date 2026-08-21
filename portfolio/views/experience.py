from django.views.generic import TemplateView
from portfolio.models import Experience, SiteSettings

class ExperienceView(TemplateView):
    template_name = "pages/experience.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experiences"] = Experience.objects.order_by("-start_date")
        context["site_settings"] = SiteSettings.objects.first()
        return context

experience_view = ExperienceView.as_view()