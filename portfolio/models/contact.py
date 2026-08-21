from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    BUDGET_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("custom", "Custom"),
    ]

    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(max_length=200, verbose_name=_("Subject"))
    service = models.ForeignKey(
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_messages",
        verbose_name=_("Service"),
    )
    budget = models.CharField(
        max_length=20,
        choices=BUDGET_CHOICES,
        default="custom",
        verbose_name=_("Budget"),
    )
    message = models.TextField(verbose_name=_("Message"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"