from django.db import models
from django.utils.translation import gettext_lazy as _


class Experience(models.Model):
    EXPERIENCE_TYPES = [
        ("professional", _("Professional")),
        ("freelance", _("Freelance")),
        ("academic", _("Academic")),
        ("personal", _("Personal")),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    organization = models.CharField(max_length=200, verbose_name=_("Organization"))
    location = models.CharField(max_length=100, verbose_name=_("Location"), blank=True)
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(
        verbose_name=_("End Date"), null=True, blank=True
    )
    is_current = models.BooleanField(default=False, verbose_name=_("Is Current"))
    type = models.CharField(
        max_length=20,
        choices=EXPERIENCE_TYPES,
        default="professional",
        verbose_name=_("Type"),
    )

    # Rich content
    role = models.TextField(
        verbose_name=_("Role"),
        help_text=_("What was my role in this position."),
        blank=True,
    )
    description = models.TextField(verbose_name=_("Description"), blank=True)
    responsibilities = models.TextField(
        verbose_name=_("Responsibilities"),
        help_text=_("Key responsibilities in this role."),
        blank=True,
    )
    tasks = models.TextField(
        verbose_name=_("Tasks"),
        help_text=_("Concrete tasks performed."),
        blank=True,
    )
    achievements = models.TextField(
        verbose_name=_("Achievements"),
        help_text=_("What was accomplished."),
        blank=True,
    )
    results = models.TextField(
        verbose_name=_("Results"),
        help_text=_("Impact and results when available."),
        blank=True,
    )

    # Relations
    related_projects = models.ManyToManyField(
        "Project",
        blank=True,
        related_name="experiences",
        verbose_name=_("Related Projects"),
    )
    technologies = models.ManyToManyField(
        "Technology",
        blank=True,
        related_name="experiences",
        verbose_name=_("Technologies"),
    )

    # Display
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))
    is_published = models.BooleanField(default=True, verbose_name=_("Is Published"))

    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} at {self.organization}"

    def get_duration(self):
        """Calculate duration from dates."""
        from datetime import date
        start = self.start_date
        end = self.end_date if self.end_date else date.today()
        
        months = (end.year - start.year) * 12 + (end.month - start.month)
        years = months // 12
        remaining_months = months % 12
        
        parts = []
        if years > 0:
            parts.append(f"{years}Y")
        if remaining_months > 0:
            parts.append(f"{remaining_months}M")
        
        return " ".join(parts) if parts else "—"
