from django.views.generic import TemplateView
from portfolio.models import Profile, Skill, SkillCategory, SiteSettings

class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["skills"] = Skill.objects.filter(is_active=True).order_by("display_order")
        context["skill_categories"] = SkillCategory.objects.order_by("display_order")
        context["site_settings"] = SiteSettings.objects.first()
        return context

about_view = AboutView.as_view()