from django.urls import reverse
from django.conf import settings
from portfolio.models import SEO


def get_seo_meta(page=None, obj=None):
    """
    Récupère les métadonnées SEO pour une page ou un objet spécifique.
    
    Args:
        page (str): Le nom de la page (ex: 'home', 'about').
        obj: Un objet spécifique (ex: Article, Project) avec des champs SEO.
    
    Returns:
        dict: Un dictionnaire contenant les métadonnées SEO.
    """
    seo_data = {
        "title": settings.SITE_NAME,
        "description": settings.SITE_DESCRIPTION,
    }
    
    # Vérifier si un objet avec des métadonnées SEO est fourni
    if obj and hasattr(obj, 'seo_title') and obj.seo_title:
        seo_data["title"] = obj.seo_title
    if obj and hasattr(obj, 'seo_description') and obj.seo_description:
        seo_data["description"] = obj.seo_description
    
    # Vérifier si une page spécifique est demandée
    if page:
        seo_obj = SEO.objects.filter(page=page).first()
        if seo_obj:
            seo_data["title"] = seo_obj.seo_title
            seo_data["description"] = seo_obj.seo_description
    
    return seo_data


def get_open_graph_meta(page=None, obj=None, request=None):
    """
    Récupère les métadonnées Open Graph pour une page ou un objet spécifique.
    
    Args:
        page (str): Le nom de la page.
        obj: Un objet spécifique (ex: Article, Project).
        request: La requête HTTP pour générer les URLs absolues.
    
    Returns:
        dict: Un dictionnaire contenant les métadonnées Open Graph.
    """
    og_data = {
        "title": settings.SITE_NAME,
        "description": settings.SITE_DESCRIPTION,
        "type": "website",
        "url": request.build_absolute_uri() if request else "",
        "image": "",
    }
    
    # Vérifier si un objet avec des métadonnées Open Graph est fourni
    if obj:
        if hasattr(obj, 'seo_title') and obj.seo_title:
            og_data["title"] = obj.seo_title
        if hasattr(obj, 'seo_description') and obj.seo_description:
            og_data["description"] = obj.seo_description
        if hasattr(obj, 'cover_image') and obj.cover_image:
            if request:
                og_data["image"] = request.build_absolute_uri(obj.cover_image.url)
            else:
                og_data["image"] = obj.cover_image.url if obj.cover_image else ""
    
    # Vérifier si une page spécifique est demandée
    if page:
        seo_obj = SEO.objects.filter(page=page).first()
        if seo_obj:
            og_data["title"] = seo_obj.seo_title
            og_data["description"] = seo_obj.seo_description
            if seo_obj.og_image:
                if request:
                    og_data["image"] = request.build_absolute_uri(seo_obj.og_image.url)
                else:
                    og_data["image"] = seo_obj.og_image.url
    
    # Si aucune image n'est définie, utiliser l'image Open Graph par défaut
    if not og_data["image"]:
        from portfolio.models import BrandingSettings
        branding = BrandingSettings.objects.first()
        if branding and branding.og_image:
            if request:
                og_data["image"] = request.build_absolute_uri(branding.og_image.url)
            else:
                og_data["image"] = branding.og_image.url
    
    return og_data


def get_canonical_url(request, obj=None):
    """
    Génère l'URL canonique pour une page ou un objet.
    
    Args:
        request: La requête HTTP.
        obj: Un objet avec une méthode get_absolute_url().
    
    Returns:
        str: L'URL canonique.
    """
    if obj and hasattr(obj, 'get_absolute_url'):
        return request.build_absolute_uri(obj.get_absolute_url())
    return request.build_absolute_uri()


def get_structured_data(page=None, obj=None, request=None):
    """
    Génère des données structurées (JSON-LD) pour le SEO.
    
    Args:
        page (str): Le type de page (ex: 'article', 'project').
        obj: L'objet pour lequel générer les données structurées.
        request: La requête HTTP.
    
    Returns:
        str: Le script JSON-LD pour les données structurées.
    """
    structured_data = {
        "@context": "https://schema.org",
    }
    
    if page == "article" and obj:
        structured_data.update({
            "@type": "Article",
            "headline": obj.title if hasattr(obj, 'title') else "",
            "description": obj.excerpt if hasattr(obj, 'excerpt') else "",
            "datePublished": obj.published_at.isoformat() if hasattr(obj, 'published_at') and obj.published_at else "",
            "dateModified": obj.updated_at.isoformat() if hasattr(obj, 'updated_at') and obj.updated_at else "",
            "author": {
                "@type": "Person",
                "name": obj.author.full_name if hasattr(obj, 'author') and obj.author else "Steve Satcheme",
            },
            "publisher": {
                "@type": "Organization",
                "name": settings.SITE_NAME,
                "logo": {
                    "@type": "ImageObject",
                    "url": request.build_absolute_uri("/static/images/logo.png") if request else "/static/images/logo.png",
                },
            },
        })
        
        if hasattr(obj, 'cover_image') and obj.cover_image:
            structured_data["image"] = request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
    
    elif page == "project" and obj:
        structured_data.update({
            "@type": "CreativeWork",
            "name": obj.title if hasattr(obj, 'title') else "",
            "description": obj.short_description if hasattr(obj, 'short_description') else "",
            "dateCreated": obj.created_at.isoformat() if hasattr(obj, 'created_at') and obj.created_at else "",
            "dateModified": obj.updated_at.isoformat() if hasattr(obj, 'updated_at') and obj.updated_at else "",
        })
        
        if hasattr(obj, 'cover_image') and obj.cover_image:
            structured_data["image"] = request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
    
    elif page == "profile":
        profile = obj if obj else None
        structured_data.update({
            "@type": "Person",
            "name": profile.full_name if profile and hasattr(profile, 'full_name') else "Steve Satcheme",
            "description": profile.biography if profile and hasattr(profile, 'biography') else "",
            "address": {
                "@type": "Place",
                "addressLocality": profile.city if profile and hasattr(profile, 'city') else "Douala",
                "addressCountry": profile.country if profile and hasattr(profile, 'country') else "Cameroon",
            },
        })
    
    else:
        structured_data.update({
            "@type": "WebSite",
            "name": settings.SITE_NAME,
            "description": settings.SITE_DESCRIPTION,
            "url": request.build_absolute_uri() if request else "",
        })
    
    # Convertir en script JSON-LD
    import json
    return f'<script type="application/ld+json">{json.dumps(structured_data, indent=2)}</script>'