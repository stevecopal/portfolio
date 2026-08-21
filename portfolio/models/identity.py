from django.db import models
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"))
    professional_name = models.CharField(max_length=100, verbose_name=_("Professional Name"))
    professional_title = models.CharField(max_length=200, verbose_name=_("Professional Title"))
    short_bio = models.TextField(verbose_name=_("Short Bio"))
    biography = models.TextField(verbose_name=_("Biography"))
    profile_image = models.ImageField(
        upload_to="profile/",
        verbose_name=_("Profile Image"),
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=100, verbose_name=_("Location"))
    country = models.CharField(max_length=100, verbose_name=_("Country"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"), null=True, blank=True)
    whatsapp = models.CharField(max_length=20, verbose_name=_("WhatsApp"), null=True, blank=True)
    availability_status = models.BooleanField(default=True, verbose_name=_("Available"))
    availability_message = models.CharField(
        max_length=200,
        verbose_name=_("Availability Message"),
        null=True,
        blank=True,
    )
    resume_file = models.FileField(
        upload_to="resume/",
        verbose_name=_("Resume File"),
        null=True,
        blank=True,
    )
    logo = models.ImageField(
        upload_to="branding/",
        verbose_name=_("Logo"),
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.full_name