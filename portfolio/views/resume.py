from django.views.generic import TemplateView
from portfolio.models import (
    Profile,
    Skill,
    SkillCategory,
    Experience,
    Project,
    SocialLink,
)

class ResumeView(TemplateView):
    template_name = "pages/resume.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["skill_categories"] = SkillCategory.objects.prefetch_related('skills').order_by('display_order')
        context["experiences"] = Experience.objects.order_by('-start_date')
        context["featured_projects"] = Project.objects.filter(is_featured=True, is_published=True).order_by('-project_date')[:5]
        context["social_links"] = SocialLink.objects.filter(is_active=True).order_by('display_order')
        return context

resume_view = ResumeView.as_view()