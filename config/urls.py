"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from portfolio.sitemaps import sitemaps
from portfolio.views.seo import robots_txt


urlpatterns = [
    # Fichiers techniques SEO (hors préfixe de langue)
    path("robots.txt", robots_txt, name="robots_txt"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # La racine redirige (301) vers la langue principale du site
    path(
        "",
        RedirectView.as_view(
            url=f"/{settings.LANGUAGE_CODE.split('-')[0]}/", permanent=True
        ),
        name="root_redirect",
    ),
    path("admin/", admin.site.urls),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("portfolio.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
)

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
