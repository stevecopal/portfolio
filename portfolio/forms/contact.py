from django import forms
from django.utils.translation import gettext_lazy as _
from portfolio.models import Service


class ContactForm(forms.Form):
    BUDGET_CHOICES = [
        ("", _("Select Budget")),
        ("low", _("Low ($1K - $5K)")),
        ("medium", _("Medium ($5K - $20K)")),
        ("high", _("High ($20K+)")),
        ("custom", _("Custom Project")),
    ]

    first_name = forms.CharField(
        label=_("First Name"),
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Your first name"),
        })
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Your last name"),
        })
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": _("your@email.com"),
        })
    )
    subject = forms.CharField(
        label=_("Subject"),
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Your subject"),
        })
    )
    service = forms.ModelChoiceField(
        label=_("Service"),
        queryset=Service.objects.filter(is_active=True).order_by("display_order"),
        required=False,
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )
    budget = forms.ChoiceField(
        label=_("Budget"),
        choices=BUDGET_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": _("Tell me about your project..."),
            "rows": 5,
        })
    )
