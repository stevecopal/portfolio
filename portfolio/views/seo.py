"""Vues techniques liées au référencement.

``robots.txt`` est servi par Django (et non par un fichier statique) afin que
l'URL du sitemap soit toujours celle du domaine réellement utilisé.
"""

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=3600, public=True)
def robots_txt(request):
    """Sert ``/robots.txt`` avec l'URL du sitemap et les règles d'exploration."""
    site_url = (getattr(settings, "SITE_URL", "") or "").rstrip("/")
    content = render_to_string("robots.txt", {"site_url": site_url})
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
