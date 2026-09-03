from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug"))
    short_description = models.TextField(verbose_name=_("Short Description"))
    description = models.TextField(verbose_name=_("Description"))
    icon = models.CharField(max_length=50, verbose_name=_("Icon"), null=True, blank=True)
    image = models.ImageField(
        upload_to="services/", verbose_name=_("Image"), null=True, blank=True
    )

    # Rich content for detail page
    hero_description = models.TextField(
        verbose_name=_("Hero Description"),
        help_text=_("The main proposition shown at the top of the detail page."),
        blank=True,
    )
    problem = models.TextField(
        verbose_name=_("Problem"),
        help_text=_("Why this solution exists — the problem it solves."),
        blank=True,
    )
    audience = models.TextField(
        verbose_name=_("Audience"),
        help_text=_("Who benefits from this solution."),
        blank=True,
    )
    features = models.TextField(
        verbose_name=_("Features"),
        help_text=_("What can be built — explained in simple terms."),
        blank=True,
    )
    concrete_example = models.TextField(
        verbose_name=_("Concrete Example"),
        help_text=_("A concrete example to help the prospect visualize."),
        blank=True,
    )
    how_it_works = models.TextField(
        verbose_name=_("How It Works"),
        help_text=_("Step-by-step explanation of how the solution works."),
        blank=True,
    )
    before_after = models.TextField(
        verbose_name=_("Before / After"),
        help_text=_("The transformation this solution enables."),
        blank=True,
    )
    benefits = models.TextField(
        verbose_name=_("Benefits"),
        help_text=_("What the client gains."),
        blank=True,
    )
    included = models.TextField(
        verbose_name=_("What's Included"),
        help_text=_("Scope of the solution."),
        blank=True,
    )
    technical_details = models.TextField(
        verbose_name=_("Technical Details"),
        help_text=_("Secondary technical information for interested visitors."),
        blank=True,
    )

    # Display
    is_featured = models.BooleanField(default=False, verbose_name=_("Is Featured"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["display_order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ServiceFeature(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="feature_items",
        verbose_name=_("Service"),
    )
    feature = models.CharField(max_length=200, verbose_name=_("Feature"))
    description = models.TextField(
        verbose_name=_("Description"), null=True, blank=True
    )
    display_order = models.PositiveIntegerField(
        default=0, verbose_name=_("Display Order")
    )

    class Meta:
        verbose_name = _("Service Feature")
        verbose_name_plural = _("Service Features")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.service.title} - {self.feature}"
