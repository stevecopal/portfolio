from django.shortcuts import render
from django.views.generic import TemplateView
from portfolio.models import (
    Profile,
    SocialLink,
    Statistic,
    Service,
    Skill,
    Project,
    Article,
    Testimonial,
    SiteSettings,
)

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["social_links"] = SocialLink.objects.filter(is_active=True).order_by("display_order")
        context["statistics"] = Statistic.objects.filter(is_active=True).order_by("display_order")
        context["featured_services"] = Service.objects.filter(is_featured=True, is_active=True).order_by("display_order")[:3]
        context["featured_skills"] = Skill.objects.filter(is_featured=True, is_active=True).order_by("display_order")[:6]
        context["featured_projects"] = Project.objects.filter(is_featured=True, is_published=True).order_by("-project_date")[:3]
        context["latest_articles"] = Article.objects.filter(status="published").order_by("-published_at")[:3]
        context["testimonials"] = Testimonial.objects.filter(is_active=True).order_by("display_order")[:3]
        context["site_settings"] = SiteSettings.objects.first()
        return context

home_view = HomeView.as_view()