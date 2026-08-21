# portfolio/utils/context_processors.py
from portfolio.models import (
    Profile,
    SocialLink,
    SiteSettings,
    Statistic,
    Service,
    Experience,
    Project,
    Article,
    Testimonial,
)

def global_context(request):
    """
    Context processor pour rendre les données globales disponibles dans tous les templates.
    Inclut :
    - Profile (identité professionnelle)
    - Branding (logos, favicon, etc.)
    - Social Links (réseaux sociaux)
    - Site Settings (paramètres du site)
    - Statistics (statistiques pour la home page)
    - Featured Services/Projects/Articles (contenu mis en avant)
    - Counts (nombre de services, projets, articles, etc.)
    """
    profile = Profile.objects.first()
    social_links = SocialLink.objects.filter(is_active=True).order_by("display_order")
    site_settings = SiteSettings.objects.first()
    
    # Statistiques
    statistics = Statistic.objects.filter(is_active=True).order_by("display_order")

    # Services
    featured_services = Service.objects.filter(is_featured=True, is_active=True).order_by("display_order")[:3]
    services_count = Service.objects.filter(is_active=True).count()
    services = Service.objects.filter(is_active=True).order_by("display_order") 

    # Projets
    featured_projects = Project.objects.filter(is_featured=True, is_published=True).order_by("-project_date")[:3]
    projects_count = Project.objects.filter(is_published=True).count()

    # Expérience
    experiences = Experience.objects.order_by("-start_date")[:5]
    experiences_count = Experience.objects.count()

    # Articles
    latest_articles = Article.objects.filter(status="published").order_by("-published_at")[:3]
    articles_count = Article.objects.filter(status="published").count()

    # Témoignages
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True).order_by("display_order")[:3]
    return {
        "profile": profile,
        "social_links": social_links,
        "site_settings": site_settings,
        "statistics": statistics,
        "featured_services": featured_services,
        "services_count": services_count,
        "featured_projects": featured_projects,
        "projects_count": projects_count,
        "experiences": experiences,
        "experiences_count": experiences_count,
        "latest_articles": latest_articles,
        "articles_count": articles_count,
        "testimonials": testimonials,
        "services": services,
    }

def seo_context(request):
    """
    Context processor pour les métadonnées SEO globales.
    """
    site_settings = SiteSettings.objects.first()
    seo = {
        "site_name": site_settings.site_name if site_settings else "Steve Satcheme | Portfolio",
        "site_description": site_settings.short_description if site_settings else "Full-Stack Developer & Digital Solutions Builder",
        "default_title": site_settings.seo_title if hasattr(site_settings, "seo_title") and site_settings.seo_title else "Steve Satcheme | Portfolio",
        "default_description": site_settings.seo_description if hasattr(site_settings, "seo_description") and site_settings.seo_description else "Full-Stack Developer & Digital Solutions Builder",
        "canonical_url": request.build_absolute_uri() if request else "",
    }
    return {"seo": seo}



def footer_services(request):
    # Récupère tous les services (tu peux filtrer avec .filter(is_active=True) si tu as ce champ)
    services = Service.objects.all()
    
    return {
        'services': services
    }