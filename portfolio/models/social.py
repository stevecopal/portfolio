from django.db import models
from django.utils.translation import gettext_lazy as _

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("whatsapp", "WhatsApp"),
    ]

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        verbose_name=_("Platform"),
    )
    url = models.URLField(verbose_name=_("URL"))
    icon = models.CharField(max_length=50, verbose_name=_("Icon"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Social Link")
        verbose_name_plural = _("Social Links")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.name} ({self.platform})"