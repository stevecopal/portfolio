from django.views.generic import TemplateView
from portfolio.models import (
    Profile,
    SocialLink,
    Service,
    Project,
    Experience,
    Testimonial,
    SiteSettings,
    Tool,
)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["social_links"] = SocialLink.objects.filter(is_active=True).order_by(
            "display_order"
        )
        context["site_settings"] = SiteSettings.objects.first()

        # Services (solutions)
        context["services"] = Service.objects.filter(is_active=True).order_by(
            "display_order"
        )

        # Featured projects (proof)
        context["featured_projects"] = (
            Project.objects.filter(is_featured=True, is_published=True)
            .prefetch_related("technologies")
            .order_by("-project_date")[:3]
        )

        # Experience (credibility)
        context["experiences"] = (
            Experience.objects.filter(is_published=True)
            .prefetch_related("related_projects", "technologies")
            .order_by("-start_date")[:3]
        )

        # Testimonials (trust)
        context["testimonials"] = (
            Testimonial.objects.filter(is_active=True)
            .order_by("display_order")[:3]
        )

        # Tools
        context["tools"] = Tool.objects.filter(is_active=True).order_by(
            "display_order", "name"
        )

        return context


home_view = HomeView.as_view()
