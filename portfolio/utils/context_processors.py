from portfolio.models import (
    Profile,
    SocialLink,
    SiteSettings,
    Service,
    Project,
    Testimonial,
)


def global_context(request):
    """Global context available in all templates."""
    profile = Profile.objects.first()
    social_links = SocialLink.objects.filter(is_active=True).order_by("display_order")
    site_settings = SiteSettings.objects.first()

    # Services
    services = Service.objects.filter(is_active=True).order_by("display_order")

    # Featured projects
    featured_projects = (
        Project.objects.filter(is_featured=True, is_published=True)
        .order_by("-project_date")[:3]
    )

    # Testimonials
    testimonials = (
        Testimonial.objects.filter(is_active=True)
        .order_by("display_order")[:3]
    )

    return {
        "profile": profile,
        "social_links": social_links,
        "site_settings": site_settings,
        "services": services,
        "featured_projects": featured_projects,
        "testimonials": testimonials,
    }


def seo_context(request):
    """SEO metadata context."""
    site_settings = SiteSettings.objects.first()
    seo = {
        "site_name": site_settings.site_name if site_settings else "Copal Satcheme",
        "site_description": (
            site_settings.short_description
            if site_settings
            else "Digital Solutions Builder"
        ),
        "default_title": (
            site_settings.seo_title
            if hasattr(site_settings, "seo_title") and site_settings.seo_title
            else "Copal Satcheme"
        ),
        "default_description": (
            site_settings.seo_description
            if hasattr(site_settings, "seo_description") and site_settings.seo_description
            else "Digital Solutions Builder"
        ),
        "canonical_url": request.build_absolute_uri() if request else "",
    }
    return {"seo": seo}
