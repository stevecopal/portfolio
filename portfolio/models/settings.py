from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name=_("Site Name"))
    slogan = models.CharField(max_length=200, verbose_name=_("Slogan"))
    short_description = models.TextField(verbose_name=_("Short Description"))
    footer_text = models.TextField(verbose_name=_("Footer Text"))
    copyright_text = models.CharField(max_length=200, verbose_name=_("Copyright Text"))
    primary_email = models.EmailField(verbose_name=_("Primary Email"))
    year = models.PositiveIntegerField(default=2026, verbose_name=_("Year"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    maintenance_mode = models.BooleanField(default=False, verbose_name=_("Maintenance Mode"))

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return self.site_name