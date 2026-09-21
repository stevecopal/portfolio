"""Plan du site XML (sitemap) destiné aux moteurs de recherche.

Particularités :

* toutes les langues du site sont déclarées (``i18n``) et chaque URL indique
  ses versions alternatives via ``<xhtml:link rel="alternate" hreflang="…">``
  (``alternates``) ;
* ``lastmod`` est renseigné à partir des données réelles (dates de mise à jour) ;
* le protocole est forcé en ``https`` pour ne jamais publier d'URL en ``http``.

Le fichier est exposé sur ``/sitemap.xml`` (voir ``config/urls.py``) et
déclaré dans ``robots.txt``.
"""

from datetime import date

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from portfolio.models import Project, Service

#: Date de dernière modification « éditoriale » des pages statiques.
#: Mettez cette date à jour quand le contenu de ces pages change.
STATIC_PAGES_LAST_MODIFIED = date(2026, 9, 21)

#: (nom d'URL, priorité, fréquence de changement) des pages statiques.
STATIC_PAGES = [
    ("home", 1.0, "weekly"),
    ("services", 0.9, "monthly"),
    ("projects", 0.9, "weekly"),
    ("about", 0.7, "monthly"),
    ("experience", 0.7, "monthly"),
    ("contact", 0.8, "monthly"),
]


class PortfolioSitemap(Sitemap):
    """Base commune à tous les sitemaps du portfolio."""

    i18n = True
    #: Ajoute les liens <xhtml:link rel="alternate" hreflang="…"> dans le sitemap.
    #: ``x_default`` reste géré dans le <head> HTML (pointe vers /fr/).
    alternates = True
    x_default = False
    protocol = "https"
    changefreq = "monthly"
    priority = 0.5
    limit = 500


class StaticViewSitemap(PortfolioSitemap):
    """Pages statiques du site (accueil, solutions, projets, contact…)."""

    def items(self):
        return [url_name for url_name, _priority, _freq in STATIC_PAGES]

    def _metadata(self, url_name):
        for name, priority, changefreq in STATIC_PAGES:
            if name == url_name:
                return priority, changefreq
        return self.priority, self.changefreq

    def location(self, item):
        return reverse(f"portfolio:{item}")

    def priority(self, item):
        return self._metadata(item)[0]

    def changefreq(self, item):
        return self._metadata(item)[1]

    def lastmod(self, item):
        return STATIC_PAGES_LAST_MODIFIED


class ProjectSitemap(PortfolioSitemap):
    """Études de cas publiées."""

    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Project.objects.filter(is_published=True).order_by("-project_date")

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, item):
        return item.updated_at


class ServiceSitemap(PortfolioSitemap):
    """Pages de services (solutions) actives."""

    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Service.objects.filter(is_active=True).order_by("display_order")

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, item):
        return item.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "services": ServiceSitemap,
}
