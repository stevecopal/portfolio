"""SEO helpers for the Copal Satcheme portfolio.

Ce module centralise tout ce qui concerne le référencement :

* métadonnées par page (``title``, ``description``, ``canonical``, ``robots``) ;
* Open Graph / Twitter Cards ;
* alternates ``hreflang`` (fr / en / x-default) ;
* données structurées JSON-LD (schema.org).

Les valeurs sont résolues dans l'ordre de priorité suivant :

1. les surcharges explicites passées par la vue (:class:`SeoMixin`) ;
2. les enregistrements du modèle :class:`portfolio.models.SEO`
   (modifiables depuis l'admin) ;
3. les objets de la page (projet, service) ;
4. les réglages ``settings.SITE_*``.
"""

import json
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse, translate_url
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from portfolio.models import Profile, SEO, Service, SocialLink

#: Longueur conseillée pour une meta description (affichée par Google).
MAX_DESCRIPTION_LENGTH = 160

#: Image de partage par défaut (1200×630), relative au dossier static.
DEFAULT_OG_IMAGE = "images/og-copal-satcheme.jpg"

#: Correspondance code langue -> valeur Open Graph ``og:locale``.
OG_LOCALES = {"fr": "fr_FR", "en": "en_US"}

#: Correspondance entre le nom d'URL Django et la clé du modèle SEO.
URL_NAME_TO_SEO_PAGE = {
    "home": "home",
    "about": "about",
    "services": "services",
    "service_detail": "services",
    "experience": "experience",
    "projects": "projects",
    "project_detail": "projects",
    "contact": "contact",
}

#: Paramètres de requête conservés dans l'URL canonique (pagination).
CANONICAL_QUERY_PARAMS = ("page",)


# ---------------------------------------------------------------------------
# Helpers génériques
# ---------------------------------------------------------------------------
def get_site_url():
    """Retourne l'URL absolue du site, sans slash final."""
    return (getattr(settings, "SITE_URL", "") or "").rstrip("/")


def absolute_url(path, request=None):
    """Transforme un chemin relatif en URL absolue (https)."""
    if not path:
        path = "/"
    if str(path).startswith(("http://", "https://")):
        return str(path)
    base = get_site_url()
    if base:
        return f"{base}{path}"
    if request is not None:
        return request.build_absolute_uri(path)
    return str(path)


def absolute_media_url(file_field, request=None):
    """Retourne l'URL absolue d'un ``FileField``/``ImageField``."""
    if not file_field:
        return ""
    try:
        url = file_field.url
    except (ValueError, AttributeError):
        return ""
    return absolute_url(url, request)


def clean_text(value, fallback=""):
    """Nettoie un texte (balises HTML retirées, espaces normalisés)."""
    text = " ".join(strip_tags(str(value or "")).split())
    return text or fallback


def truncate_description(text, length=MAX_DESCRIPTION_LENGTH):
    """Tronque proprement un texte destiné à une meta description."""
    text = clean_text(text)
    if len(text) <= length:
        return text
    cut = text[: length - 1]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return f"{cut.rstrip(' ,;:.')}…"


def current_language():
    """Code langue actif, sans variante régionale (``fr-ca`` -> ``fr``)."""
    return (get_language() or settings.LANGUAGE_CODE).split("-")[0]


def default_language():
    """Langue par défaut du site (utilisée pour ``x-default``)."""
    return settings.LANGUAGE_CODE.split("-")[0]


def og_locale(language_code=None):
    """Retourne la valeur ``og:locale`` correspondant à une langue."""
    code = (language_code or current_language()).split("-")[0]
    return OG_LOCALES.get(code, code)


def get_site_name():
    """Nom commercial utilisé dans les métadonnées."""
    return getattr(settings, "SITE_NAME", "") or "Copal Satcheme"


def get_alternate_names():
    """Variantes du nom utilisées pour les recherches de marque."""
    names = getattr(settings, "SITE_ALTERNATE_NAMES", None) or []
    return [name for name in names if name]


def get_seo_record(page):
    """Récupère un enregistrement SEO, sans jamais casser le rendu d'une page."""
    if not page:
        return None
    try:
        return SEO.objects.filter(page=page).first()
    except Exception:  # pragma: no cover - dépend de la base de données
        return None


def get_profile():
    """Retourne le profil unique du site (ou ``None``)."""
    try:
        return Profile.objects.first()
    except Exception:  # pragma: no cover
        return None


def get_social_links():
    """Retourne les liens sociaux actifs (utilisés pour ``sameAs``)."""
    try:
        return list(SocialLink.objects.filter(is_active=True).order_by("display_order"))
    except Exception:  # pragma: no cover
        return []


def get_page_key(request):
    """Déduit la clé du modèle SEO à partir de l'URL courante."""
    if request is None:
        return None
    match = getattr(request, "resolver_match", None)
    url_name = getattr(match, "url_name", None) if match else None
    return URL_NAME_TO_SEO_PAGE.get(url_name)


def get_active_services():
    """Retourne les services actifs (catalogue ``schema.org``)."""
    try:
        return list(Service.objects.filter(is_active=True).order_by("display_order"))
    except Exception:  # pragma: no cover
        return []


def canonical_url(request, path=None):
    """Construit l'URL canonique absolue de la page courante.

    Les paramètres de filtrage (``?tech=``, ``?lang=``…) sont ignorés afin
    d'éviter le contenu dupliqué. Seule la pagination est conservée.
    """
    target = path or (request.path if request is not None else "/")
    query = ""
    if request is not None:
        params = {
            key: value
            for key, value in request.GET.items()
            if key in CANONICAL_QUERY_PARAMS and value
        }
        query = urlencode(params)
    return absolute_url(f"{target}?{query}" if query else target, request)


def build_alternates(request, path=None):
    """Construit les liens ``hreflang`` pour toutes les langues du site."""
    if request is None:
        return []
    target = path or request.path
    alternates = []
    for code, _label in settings.LANGUAGES:
        alternates.append(
            {
                "hreflang": code,
                "href": absolute_url(translate_url(target, code), request),
            }
        )
    alternates.append(
        {
            "hreflang": "x-default",
            "href": absolute_url(translate_url(target, default_language()), request),
        }
    )
    return alternates


def default_og_image(request=None):
    """URL absolue de l'image de partage par défaut."""
    from django.templatetags.static import static

    return absolute_url(static(DEFAULT_OG_IMAGE), request)


def as_datetime(value):
    """Convertit une date en datetime compatible avec ``og:article``."""
    if not value:
        return None
    if isinstance(value, timezone.datetime):
        if timezone.is_aware(value):
            return value
        return timezone.make_aware(value)
    return timezone.make_aware(
        timezone.datetime.combine(value, timezone.datetime.min.time())
    )


# ---------------------------------------------------------------------------
# Données structurées (JSON-LD / schema.org)
# ---------------------------------------------------------------------------
def dump_json_ld(data):
    """Sérialise une donnée structurée en JSON sûr pour une balise <script>."""
    payload = json.dumps(data, ensure_ascii=False, default=str)
    return (
        payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    )


def json_ld_script(data):
    """Retourne la balise ``<script type="application/ld+json">`` complète."""
    return f'<script type="application/ld+json">{dump_json_ld(data)}</script>'


def country_code(country_name):
    """Convertit un nom de pays en code ISO 3166-1 alpha-2."""
    mapping = {
        "cameroun": "CM",
        "cameroon": "CM",
        "cm": "CM",
        "france": "FR",
        "fr": "FR",
        "canada": "CA",
        "belgique": "BE",
        "belgium": "BE",
    }
    if not country_name:
        return ""
    return mapping.get(str(country_name).strip().lower(), str(country_name).strip())


def postal_address_data(profile=None):
    """Adresse postale au format schema.org."""
    profile = profile if profile is not None else get_profile()
    if not profile:
        return None
    data = {"@type": "PostalAddress"}
    if profile.city:
        data["addressLocality"] = profile.city
    if profile.location:
        data["streetAddress"] = profile.location
    code = country_code(profile.country)
    if code:
        data["addressCountry"] = code
    return data if len(data) > 1 else None


def person_reference():
    """Référence ``@id`` vers la personne (évite la duplication du nœud)."""
    return {"@id": f"{get_site_url()}/#person"}


def person_data(profile=None, request=None):
    """La personne propriétaire du site, au format schema.org."""
    profile = profile if profile is not None else get_profile()
    services = get_active_services()
    data = {
        "@type": "Person",
        "@id": f"{get_site_url()}/#person",
        "name": (profile.full_name if profile else "") or get_site_name(),
        "url": absolute_url("/", request),
    }
    alternate_names = get_alternate_names()
    if alternate_names:
        data["alternateName"] = alternate_names
    if profile:
        if profile.professional_title:
            data["jobTitle"] = profile.professional_title
        bio = clean_text(profile.short_bio or profile.biography)
        if bio:
            data["description"] = bio
        if profile.email:
            data["email"] = profile.email
        if profile.phone:
            data["telephone"] = profile.phone
        image = absolute_media_url(profile.profile_image, request)
        if image:
            data["image"] = image
        address = postal_address_data(profile)
        if address:
            data["address"] = address
    same_as = [link.url for link in get_social_links() if link.url]
    if same_as:
        data["sameAs"] = same_as
    if services:
        data["knowsAbout"] = [service.title for service in services]
    data["knowsLanguage"] = ["fr", "en"]
    return data


def website_data(request=None):
    """Le site web, au format schema.org."""
    site_url = get_site_url()
    data = {
        "@type": "WebSite",
        "@id": f"{site_url}/#website",
        "url": f"{site_url}/" if site_url else "/",
        "name": get_site_name(),
        "description": clean_text(getattr(settings, "SITE_DESCRIPTION", "")),
        "inLanguage": current_language(),
        "publisher": person_reference(),
    }
    alternate_names = get_alternate_names()
    if alternate_names:
        data["alternateName"] = alternate_names
    return data


def professional_service_data(services=None, profile=None, request=None):
    """Activité de services (LocalBusiness) — signal fort pour le SEO local."""
    profile = profile if profile is not None else get_profile()
    services = services if services is not None else get_active_services()
    site_url = get_site_url()
    data = {
        "@type": "ProfessionalService",
        "@id": f"{site_url}/#service",
        "name": get_site_name(),
        "url": absolute_url("/", request),
        "founder": person_reference(),
        "areaServed": [{"@type": "Country", "name": "Cameroon", "identifier": "CM"}],
        "availableLanguage": ["fr", "en"],
    }
    if profile:
        if profile.professional_title:
            data["description"] = clean_text(profile.short_bio or profile.biography)
            data["slogan"] = profile.professional_title
        if profile.email:
            data["email"] = profile.email
        if profile.phone:
            data["telephone"] = profile.phone
        logo = absolute_media_url(profile.logo, request)
        image = absolute_media_url(profile.profile_image, request)
        if logo or image:
            data["image"] = logo or image
        address = postal_address_data(profile)
        if address:
            data["address"] = address
    same_as = [link.url for link in get_social_links() if link.url]
    if same_as:
        data["sameAs"] = same_as
    if services:
        data["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": _("Services numériques"),
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": service_data(service, request, full=False),
                }
                for service in services
            ],
        }
    return data


def service_data(service, request=None, full=True):
    """Un service, au format schema.org."""
    url = absolute_url(service.get_absolute_url(), request)
    data = {
        "@type": "Service",
        "@id": f"{url}#service",
        "name": service.title,
        "url": url,
        "serviceType": service.title,
        "provider": person_reference(),
        "areaServed": [{"@type": "Country", "name": "Cameroon", "identifier": "CM"}],
    }
    description = clean_text(service.hero_description or service.short_description)
    if description:
        data["description"] = truncate_description(description, 300)
    image = absolute_media_url(service.image, request)
    if image:
        data["image"] = image
    if full:
        benefits = clean_text(service.benefits)
        features = clean_text(service.features)
        if features and not data.get("description"):
            data["description"] = truncate_description(features, 300)
        if benefits:
            data["offers"] = {
                "@type": "Offer",
                "category": service.title,
                "description": truncate_description(benefits, 300),
                "availability": "https://schema.org/InStock",
                "areaServed": {
                    "@type": "Country",
                    "name": "Cameroon",
                    "identifier": "CM",
                },
            }
    return data


def project_data(project, request=None):
    """Une réalisation/projet, au format schema.org (CreativeWork)."""
    url = absolute_url(project.get_absolute_url(), request)
    data = {
        "@type": "CreativeWork",
        "@id": f"{url}#project",
        "name": project.title,
        "url": url,
        "creator": person_reference(),
        "author": person_reference(),
        "inLanguage": current_language(),
    }
    description = clean_text(project.short_description or project.description)
    if description:
        data["description"] = truncate_description(description, 300)
    image = absolute_media_url(project.cover_image, request)
    if image:
        data["image"] = image
    if project.project_date:
        data["dateCreated"] = project.project_date.isoformat()
    if project.updated_at:
        data["dateModified"] = project.updated_at.isoformat()
    technologies = [tech.name for tech in project.technologies.all()]
    if technologies:
        data["keywords"] = ", ".join(technologies)
    if project.live_url:
        data["sameAs"] = [project.live_url]
    return data


def item_list_data(items, request=None, name=""):
    """Liste d'éléments (``ItemList``) pour les pages d'index."""
    elements = [
        {
            "@type": "ListItem",
            "position": position,
            "name": item.get("name", ""),
            "url": item.get("url", ""),
        }
        for position, item in enumerate(items, start=1)
    ]
    data = {
        "@type": "ItemList",
        "numberOfItems": len(elements),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": elements,
    }
    if name:
        data["name"] = name
    return data


def breadcrumb_data(request, items):
    """Fil d'Ariane (``BreadcrumbList``).

    ``items`` est une liste de tuples ``(url_name, label)`` ; le dernier
    élément représente la page courante et peut avoir ``url_name=None``.
    Les noms d'URL peuvent être donnés avec ou sans leur namespace.
    """

    def qualified(url_name):
        return url_name if ":" in url_name else f"portfolio:{url_name}"

    elements = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": _("Accueil"),
            "item": absolute_url(reverse(qualified("home")), request),
        }
    ]
    for position, (url_name, label) in enumerate(items, start=2):
        element = {"@type": "ListItem", "position": position, "name": label}
        if url_name:
            element["item"] = absolute_url(reverse(qualified(url_name)), request)
        elements.append(element)
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def contact_page_data(request=None, profile=None):
    """La page de contact, au format schema.org."""
    profile = profile if profile is not None else get_profile()
    url = absolute_url(reverse("portfolio:contact"), request)
    data = {
        "@type": "ContactPage",
        "@id": f"{url}#contact",
        "name": _("Contact"),
        "url": url,
        "inLanguage": current_language(),
    }
    contact_point = {"@type": "ContactPoint", "contactType": "customer service"}
    if profile:
        if profile.email:
            contact_point["email"] = profile.email
        if profile.phone:
            contact_point["telephone"] = profile.phone
        contact_point["availableLanguage"] = ["fr", "en"]
        address = postal_address_data(profile)
        if address:
            data["address"] = address
    if len(contact_point) > 2:
        data["mainEntity"] = contact_point
    return data


def profile_page_data(request=None):
    """La page « à propos », au format schema.org."""
    url = absolute_url(reverse("portfolio:about"), request)
    return {
        "@type": "ProfilePage",
        "@id": f"{url}#profilepage",
        "name": _("À propos"),
        "url": url,
        "inLanguage": current_language(),
        "mainEntity": person_reference(),
    }


def experiences_data(experiences):
    """Expériences professionnelles sous forme de liste d'organisations."""
    organizations = []
    seen = set()
    for experience in experiences:
        name = (experience.organization or "").strip()
        if not name or name in seen:
            continue
        seen.add(name)
        organizations.append({"@type": "Organization", "name": name})
    if not organizations:
        return None
    return item_list_data(
        [{"name": organization["name"]} for organization in organizations],
        name=_("Parcours professionnel"),
    )


# ---------------------------------------------------------------------------
# Construction du contexte SEO d'une page
# ---------------------------------------------------------------------------
def build_seo(request, page_key=None, **overrides):
    """Construit le dictionnaire complet de métadonnées d'une page.

    Args:
        request: La requête HTTP courante (langue, chemin, paramètres).
        page_key: La clé du modèle ``SEO`` (déduite de l'URL si absente).
        **overrides: Surcharges (``title``, ``description``, ``image``,
            ``type``, ``robots``, ``breadcrumbs``, ``structured_data``,
            ``canonical``, ``image_alt``, ``og_title``, ``publish_time``,
            ``modify_time``, ``description_length``).

    Returns:
        dict: Métadonnées prêtes à être utilisées dans ``base.html``.
    """
    page_key = page_key or get_page_key(request)
    record = get_seo_record(page_key)
    profile = get_profile()
    site_name = get_site_name()

    fallback_description = (
        clean_text(getattr(settings, "SITE_DESCRIPTION", "")) or site_name
    )
    title = (
        clean_text(overrides.get("title"))
        or clean_text(record.seo_title if record else "")
        or site_name
    )
    description = truncate_description(
        overrides.get("description")
        or (record.seo_description if record else "")
        or fallback_description,
        overrides.get("description_length", MAX_DESCRIPTION_LENGTH),
    )
    canonical = overrides.get("canonical") or canonical_url(request)

    image = overrides.get("image") or ""
    if not image and record is not None:
        image = absolute_media_url(record.og_image, request)
    if not image:
        # Carte de partage de marque (1200×630) ; le logo/profil ne sert que
        # de secours si l'image par défaut est introuvable.
        image = default_og_image(request) or absolute_media_url(
            profile.logo if profile else None, request
        )

    structured_data = [person_data(profile, request), website_data(request)]
    if overrides.get("include_service_catalog"):
        structured_data.append(
            professional_service_data(request=request, profile=profile)
        )
    breadcrumbs = overrides.get("breadcrumbs")
    if breadcrumbs:
        structured_data.append(breadcrumb_data(request, breadcrumbs))
    for extra in overrides.get("structured_data") or []:
        if extra:
            structured_data.append(extra)

    language = current_language()
    return {
        "page_key": page_key,
        "title": title,
        "og_title": overrides.get("og_title") or title,
        "description": description,
        "canonical": canonical,
        "image": image,
        "image_alt": overrides.get("image_alt") or site_name,
        "type": overrides.get("type") or "website",
        "robots": overrides.get("robots") or "index, follow",
        "site_name": site_name,
        "site_url": get_site_url(),
        "locale": og_locale(language),
        "locale_alternates": [
            og_locale(code)
            for code, _label in settings.LANGUAGES
            if code.split("-")[0] != language
        ],
        "alternates": build_alternates(request),
        "structured_data": structured_data,
        "twitter_card": "summary_large_image" if image else "summary",
        "publish_time": overrides.get("publish_time"),
        "modify_time": overrides.get("modify_time"),
        "google_verification": getattr(settings, "GOOGLE_SITE_VERIFICATION", ""),
        "bing_verification": getattr(settings, "BING_SITE_VERIFICATION", ""),
    }


class SeoMixin:
    """Injecte un contexte SEO complet dans les vues basées sur des classes.

    Exemple::

        class ProjectDetailView(SeoMixin, DetailView):
            seo_page_key = "projects"

            def get_seo_overrides(self):
                return {"title": self.object.title}
    """

    #: Clé du modèle ``SEO`` à utiliser (déduite de l'URL sinon).
    seo_page_key = None

    def get_seo_page_key(self):
        return self.seo_page_key or get_page_key(self.request)

    def get_seo_overrides(self):
        """Surcharges spécifiques à la vue (titre, image, JSON-LD, ...)."""
        return {}

    def get_seo_breadcrumbs(self):
        """Fil d'Ariane : liste de ``(url_name, label)``."""
        return None

    def get_seo_context(self, **extra):
        data = dict(self.get_seo_overrides())
        data.update(extra)
        breadcrumbs = self.get_seo_breadcrumbs()
        if breadcrumbs and "breadcrumbs" not in data:
            data["breadcrumbs"] = breadcrumbs
        return build_seo(self.request, page_key=self.get_seo_page_key(), **data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seo"] = self.get_seo_context()
        return context


# ---------------------------------------------------------------------------
# API historique (conservée pour compatibilité)
# ---------------------------------------------------------------------------
def get_seo_meta(page=None, obj=None):
    """
    Récupère les métadonnées SEO pour une page ou un objet spécifique.

    Args:
        page (str): Le nom de la page (ex: 'home', 'about').
        obj: Un objet spécifique (ex: Project) avec des champs SEO.

    Returns:
        dict: Un dictionnaire contenant les métadonnées SEO.
    """
    seo_data = {
        "title": get_site_name(),
        "description": clean_text(getattr(settings, "SITE_DESCRIPTION", "")),
    }

    # Vérifier si un objet avec des métadonnées SEO est fourni
    if obj and getattr(obj, "seo_title", None):
        seo_data["title"] = obj.seo_title
    if obj and getattr(obj, "seo_description", None):
        seo_data["description"] = obj.seo_description

    # Vérifier si une page spécifique est demandée
    seo_obj = get_seo_record(page)
    if seo_obj:
        seo_data["title"] = seo_obj.seo_title
        seo_data["description"] = seo_obj.seo_description

    return seo_data


def get_open_graph_meta(page=None, obj=None, request=None):
    """
    Récupère les métadonnées Open Graph pour une page ou un objet spécifique.

    Args:
        page (str): Le nom de la page.
        obj: Un objet spécifique (ex: Project).
        request: La requête HTTP pour générer les URLs absolues.

    Returns:
        dict: Un dictionnaire contenant les métadonnées Open Graph.
    """
    meta = get_seo_meta(page=page, obj=obj)
    og_data = {
        "title": meta["title"],
        "description": meta["description"],
        "type": "website",
        "url": canonical_url(request) if request is not None else "",
        "image": "",
    }

    if obj is not None and getattr(obj, "cover_image", None):
        og_data["image"] = absolute_media_url(obj.cover_image, request)

    seo_obj = get_seo_record(page)
    if seo_obj is not None and seo_obj.og_image:
        og_data["image"] = absolute_media_url(seo_obj.og_image, request)

    # Si aucune image n'est définie, utiliser l'image Open Graph par défaut
    if not og_data["image"]:
        og_data["image"] = default_og_image(request)

    return og_data


def get_canonical_url(request, obj=None):
    """
    Génère l'URL canonique absolue de la page ou de l'objet courant.
    """
    if obj is not None and hasattr(obj, "get_absolute_url"):
        return absolute_url(obj.get_absolute_url(), request)
    return canonical_url(request)


def get_structured_data(page=None, obj=None, request=None):
    """
    Génère des données structurées (JSON-LD) pour le SEO.

    Args:
        page (str): Le type de page (ex: 'project', 'service', 'profile').
        obj: L'objet pour lequel générer les données structurées.
        request: La requête HTTP.

    Returns:
        str: Le script JSON-LD pour les données structurées.
    """
    if page == "project" and obj is not None:
        return json_ld_script(project_data(obj, request))
    if page == "service" and obj is not None:
        return json_ld_script(service_data(obj, request))
    if page == "profile":
        return json_ld_script(person_data(obj, request))
    if page == "contact":
        return json_ld_script(contact_page_data(request))
    return json_ld_script(website_data(request))
