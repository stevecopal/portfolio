"""Balises et filtres de template liés au référencement (SEO)."""

from django import template
from django.utils.safestring import mark_safe

from portfolio.utils.seo import absolute_url, dump_json_ld

register = template.Library()


@register.filter(name="json_ld")
def json_ld(value):
    """Sérialise une donnée structurée (dict) en JSON sûr pour un <script>."""
    return mark_safe(dump_json_ld(value))


@register.simple_tag
def seo_absolute_url(path):
    """Transforme un chemin relatif en URL absolue (domaine du site)."""
    return absolute_url(path)


@register.simple_tag(takes_context=True)
def translation_href(context, language_code):
    """Retourne l'URL absolue de la page courante dans une autre langue."""
    from django.urls import translate_url

    request = context.get("request")
    if request is None:
        return ""
    return absolute_url(translate_url(request.path, language_code), request)
