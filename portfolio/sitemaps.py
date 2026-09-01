from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from portfolio.models import Article, Project, Service

class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return [
            'portfolio:home',
            'portfolio:about',
            'portfolio:services',
            'portfolio:projects',
            'portfolio:experience',
            'portfolio:blog',
            'portfolio:contact',
        ]

    def location(self, item):
        return reverse(item)

class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Article.objects.filter(status='published')

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_published=True)

class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Service.objects.filter(is_active=True)

# Combine tous les sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'articles': ArticleSitemap,
    'projects': ProjectSitemap,
    'services': ServiceSitemap,
}