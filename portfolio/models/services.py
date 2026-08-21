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
        upload_to="services/",
        verbose_name=_("Image"),
        null=True,
        blank=True,
    )
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
        related_name="features",
        verbose_name=_("Service"),
    )
    feature = models.CharField(max_length=200, verbose_name=_("Feature"))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Service Feature")
        verbose_name_plural = _("Service Features")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.service.title} - {self.feature}"