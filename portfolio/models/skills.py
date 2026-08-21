from django.db import models
from django.utils.translation import gettext_lazy as _

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Skill Category")
        verbose_name_plural = _("Skill Categories")
        ordering = ["display_order"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="skills",
        verbose_name=_("Category"),
    )
    icon = models.CharField(max_length=50, verbose_name=_("Icon"), null=True, blank=True)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="intermediate",
        verbose_name=_("Level"),
    )
    years_experience = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Years of Experience"),
    )
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Is Featured"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.name} ({self.level})"