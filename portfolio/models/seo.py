from django.db import models
from django.utils.translation import gettext_lazy as _

class SEO(models.Model):
    page = models.CharField(max_length=100, unique=True, verbose_name=_("Page"))
    seo_title = models.CharField(max_length=200, verbose_name=_("SEO Title"))
    seo_description = models.TextField(verbose_name=_("SEO Description"))
    canonical_url = models.URLField(verbose_name=_("Canonical URL"), null=True, blank=True)
    og_image = models.ImageField(
        upload_to="seo/",
        verbose_name=_("Open Graph Image"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("SEO")
        verbose_name_plural = _("SEO")

    def __str__(self):
        return self.page