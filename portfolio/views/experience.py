from django.views.generic import TemplateView
from portfolio.models import Experience, Profile, SiteSettings


class ExperienceView(TemplateView):
    template_name = "pages/experience.html"

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
