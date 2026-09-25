from django.conf import settings

from portfolio.models import (
    Profile,
    SocialLink,
    SiteSettings,
    Service,
    Project,
    Testimonial,
)

from .seo import build_seo


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
        .order_by("display_order")[:10]
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
    """Métadonnées SEO de la page courante (titre, description, JSON-LD…).

    Contexte utilisé par ``base.html``. Les vues qui héritent de
    :class:`portfolio.utils.seo.SeoMixin` fournissent une version enrichie
    (projet, service, fil d'Ariane…) qui écrase cette valeur par défaut.
    """
    try:
        seo = build_seo(request)
    except Exception:  # pragma: no cover - ne doit jamais casser une page
        seo = {
            "title": getattr(settings, "SITE_NAME", "Copal Satcheme"),
            "description": getattr(settings, "SITE_DESCRIPTION", ""),
            "canonical": "",
            "image": "",
            "type": "website",
            "robots": "index, follow",
            "alternates": [],
            "structured_data": [],
            "locale": "",
            "locale_alternates": [],
            "site_name": getattr(settings, "SITE_NAME", "Copal Satcheme"),
            "site_url": getattr(settings, "SITE_URL", ""),
            "twitter_card": "summary",
        }
    return {
        "seo": seo,
        "site_url": getattr(settings, "SITE_URL", ""),
        "site_verification": {
            "google": getattr(settings, "GOOGLE_SITE_VERIFICATION", ""),
            "bing": getattr(settings, "BING_SITE_VERIFICATION", ""),
        },
    }

