from django.db import models
from django.utils.translation import gettext_lazy as _

class Statistic(models.Model):
    label = models.CharField(max_length=100, verbose_name=_("Label"))
    value = models.PositiveIntegerField(verbose_name=_("Value"))
    icon = models.CharField(max_length=50, verbose_name=_("Icon"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Statistic")
        verbose_name_plural = _("Statistics")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.label}: {self.value}"