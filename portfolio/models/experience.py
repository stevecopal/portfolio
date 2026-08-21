from django.db import models
from django.utils.translation import gettext_lazy as _

class Experience(models.Model):
    EXPERIENCE_TYPES = [
        ("professional", "Professional"),
        ("freelance", "Freelance"),
        ("academic", "Academic"),
        ("personal", "Personal"),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    company = models.CharField(max_length=200, verbose_name=_("Company"))
    location = models.CharField(max_length=100, verbose_name=_("Location"))
    description = models.TextField(verbose_name=_("Description"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(
        verbose_name=_("End Date"),
        null=True,
        blank=True,
    )
    is_current = models.BooleanField(default=False, verbose_name=_("Is Current"))
    type = models.CharField(
        max_length=20,
        choices=EXPERIENCE_TYPES,
        default="professional",
        verbose_name=_("Type"),
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} at {self.company}"