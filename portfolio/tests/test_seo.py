"""Tests du référencement (SEO) : métadonnées, sitemap, robots.txt, JSON-LD."""

import json
import re
import xml.etree.ElementTree as ET

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from portfolio.models import Profile, Project, SEO, Service


class SeoMetaTestCase(TestCase):
    """Vérifie les balises SEO des pages publiques."""

    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(
            full_name="Test Satcheme",
            professional_name="Test Satcheme",
            professional_title="Developpeur Full-Stack",
            short_bio="Developpeur full-stack au Cameroun.",
            biography="Developpeur full-stack au Cameroun, specialise en Django.",
            location="Bafoussam",
            country="Cameroon",
            city="Bafoussam",
            email="test@example.com",
        )
        cls.service = Service.objects.create(
            title="Developpement Web",
            slug="developpement-web",
            short_description="Applications web sur mesure.",
            description="Applications web sur mesure.",
        )
        cls.project = Project.objects.create(
            title="Projet Test",
            slug="projet-test",
            short_description="Un projet de test.",
            project_date="2025-01-15",
        )
        SEO.objects.create(
            page="home",
            seo_title="Titre SEO Accueil | Test",
            seo_description="Description SEO accueil unique.",
        )

    def get_html(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"{url} ne repond pas 200")
        return response.content.decode()

    def json_ld_types(self, html):
        return [
            json.loads(block).get("@type")
            for block in re.findall(
                r'<script type="application/ld\+json">(.*?)</script>', html, re.S
            )
        ]

    def test_pages_repondent_200(self):
        for name in ["home", "about", "services", "experience", "projects", "contact"]:
            with self.subTest(page=name):
                self.assertEqual(
                    self.client.get(reverse(f"portfolio:{name}")).status_code, 200
                )

    def test_titre_et_description_utilisent_le_modele_seo(self):
        html = self.get_html(reverse("portfolio:home"))
        self.assertIn("<title>Titre SEO Accueil | Test</title>", html)
        self.assertIn(
            '<meta name="description" content="Description SEO accueil unique.">', html
        )

    def test_une_seule_balise_title_par_page(self):
        for name in ["home", "about", "services", "projects", "contact"]:
            with self.subTest(page=name):
                html = self.get_html(reverse(f"portfolio:{name}"))
                self.assertEqual(len(re.findall(r"<title>", html)), 1)

    def test_canonical_absolue_en_https(self):
        for name in ["home", "services", "projects"]:
            url = reverse(f"portfolio:{name}")
            html = self.get_html(url)
            canonical = re.search(r'rel="canonical" href="([^"]+)"', html).group(1)
            self.assertTrue(canonical.startswith(settings.SITE_URL))
            self.assertTrue(canonical.endswith(url))

    def test_hreflang_fr_en_et_x_default(self):
        html = self.get_html(reverse("portfolio:home"))
        self.assertIn('hreflang="fr"', html)
        self.assertIn('hreflang="en"', html)
        self.assertIn('hreflang="x-default"', html)
        self.assertIn(f'href="{settings.SITE_URL}/fr/"', html)
        self.assertIn(f'href="{settings.SITE_URL}/en/"', html)

    def test_open_graph_complet(self):
        url = reverse("portfolio:projects")
        html = self.get_html(url)
        self.assertIn('property="og:title"', html)
        self.assertIn('property="og:description"', html)
        self.assertIn('property="og:site_name"', html)
        self.assertIn('property="og:locale"', html)
        self.assertIn('property="og:image"', html)
        self.assertIn('name="twitter:card"', html)
        og_url = re.search(r'property="og:url" content="([^"]+)"', html).group(1)
        self.assertTrue(og_url.endswith(url))

    def test_donnees_structurees_json_valides(self):
        html = self.get_html(reverse("portfolio:home"))
        types = self.json_ld_types(html)
        self.assertGreaterEqual(len(types), 2)
        self.assertIn("Person", types)
        self.assertIn("WebSite", types)

    def test_projet_a_un_titre_dynamique_et_des_donnees_structurees(self):
        html = self.get_html(self.project.get_absolute_url())
        self.assertIn("Projet Test", html)
        types = self.json_ld_types(html)
        self.assertIn("CreativeWork", types)
        self.assertIn("BreadcrumbList", types)

    def test_service_a_des_donnees_structurees_service(self):
        html = self.get_html(self.service.get_absolute_url())
        self.assertIn("Service", self.json_ld_types(html))

    def test_page_404_renvoie_404_et_noindex(self):
        response = self.client.get("/fr/page-inexistante/")
        self.assertEqual(response.status_code, 404)
        self.assertIn("noindex", response.content.decode())

    def test_racine_redirige_vers_la_langue_principale(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], f"/{settings.LANGUAGE_CODE}/")

    def test_parametre_lang_redirige_vers_url_propre(self):
        response = self.client.get("/fr/contact/?lang=en")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/en/contact/")

    def test_canonical_ignore_les_filtres(self):
        html = self.get_html(reverse("portfolio:projects") + "?tech=django")
        canonical = re.search(r'rel="canonical" href="([^"]+)"', html).group(1)
        self.assertNotIn("tech=", canonical)


class RobotsTxtTestCase(TestCase):
    def test_robots_txt_est_servi_par_django(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response["Content-Type"])
        content = response.content.decode()
        self.assertIn("User-agent: *", content)
        self.assertIn(f"Sitemap: {settings.SITE_URL}/sitemap.xml", content)
        self.assertIn("Disallow: /admin/", content)
        self.assertNotIn("ton-domain.com", content)


class SitemapTestCase(TestCase):
    NAMESPACES = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xhtml": "http://www.w3.org/1999/xhtml",
    }

    #: Le domaine des URL du sitemap est celui de la requête (comportement
    #: Django standard) ; les tests utilisent l'hôte « testserver ».
    SITE_PREFIX = "https://testserver"

    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            title="Projet Sitemap",
            slug="projet-sitemap",
            short_description="Description.",
            project_date="2025-02-01",
            is_published=True,
        )
        cls.hidden = Project.objects.create(
            title="Projet Masque",
            slug="projet-masque",
            short_description="Description.",
            project_date="2025-02-01",
            is_published=False,
        )
        cls.service = Service.objects.create(
            title="Service Sitemap",
            slug="service-sitemap",
            short_description="Description.",
            description="Description.",
        )

    def get_locations(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        root = ET.fromstring(response.content)
        return [
            node.text for node in root.findall("sm:url/sm:loc", self.NAMESPACES)
        ], root

    def test_sitemap_valide_et_en_https(self):
        urls, _root = self.get_locations()
        self.assertTrue(urls)
        for url in urls:
            self.assertTrue(url.startswith("https://"), url)

    def test_sitemap_contient_toutes_les_langues(self):
        urls, _root = self.get_locations()
        self.assertIn(f"{self.SITE_PREFIX}/fr/", urls)
        self.assertIn(f"{self.SITE_PREFIX}/en/", urls)
        self.assertIn(f"{self.SITE_PREFIX}/fr/about/", urls)

    def test_sitemap_contient_projets_et_services_publies(self):
        urls, _root = self.get_locations()
        self.assertIn(f"{self.SITE_PREFIX}{self.project.get_absolute_url()}", urls)
        self.assertIn(f"{self.SITE_PREFIX}{self.service.get_absolute_url()}", urls)
        self.assertNotIn(f"{self.SITE_PREFIX}{self.hidden.get_absolute_url()}", urls)

    def test_sitemap_declare_les_alternates_hreflang(self):
        _urls, root = self.get_locations()
        first = root.find("sm:url", self.NAMESPACES)
        languages = [
            link.get("hreflang")
            for link in first.findall("xhtml:link", self.NAMESPACES)
        ]
        self.assertIn("fr", languages)
        self.assertIn("en", languages)

    def test_sitemap_a_des_lastmod_et_priorites(self):
        _urls, root = self.get_locations()
        first = root.find("sm:url", self.NAMESPACES)
        self.assertIsNotNone(first.find("sm:lastmod", self.NAMESPACES))
        self.assertIsNotNone(first.find("sm:priority", self.NAMESPACES))
