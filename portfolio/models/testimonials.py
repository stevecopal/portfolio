from django.db import models
from django.utils.translation import gettext_lazy as _

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    position = models.CharField(max_length=100, verbose_name=_("Position"))
    company = models.CharField(max_length=100, verbose_name=_("Company"))
    photo = models.ImageField(
        upload_to="testimonials/",
        verbose_name=_("Photo"),
        null=True,
        blank=True,
    )
    testimonial = models.TextField(verbose_name=_("Testimonial"))
    rating = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Rating"),
    )
    is_featured = models.BooleanField(default=False, verbose_name=_("Is Featured"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.name} - {self.position}"