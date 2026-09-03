from django.db import models
from django.utils.translation import gettext_lazy as _


class Tool(models.Model):
    CATEGORY_CHOICES = [
        ("language", _("Language")),
        ("framework", _("Framework")),
        ("database", _("Database")),
        ("tool", _("Tool")),
        ("other", _("Other")),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    icon = models.CharField(
        max_length=50,
        verbose_name=_("Icon Class"),
        help_text=_("Font Awesome icon class (e.g., fa-python, fa-react)"),
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="tool",
        verbose_name=_("Category"),
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Tool")
        verbose_name_plural = _("Tools")
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name
