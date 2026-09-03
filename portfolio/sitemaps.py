from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from portfolio.models import Project, Service


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return [
            "portfolio:home",
            "portfolio:services",
            "portfolio:experience",
            "portfolio:projects",
            "portfolio:contact",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_published=True)


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Service.objects.filter(is_active=True)


sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "services": ServiceSitemap,
}
