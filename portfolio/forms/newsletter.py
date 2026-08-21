from django import forms
from django.utils.translation import gettext_lazy as _
from portfolio.models import NewsletterSubscriber

class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": _("Your Email"),
                "class": "w-full p-3 border border-gray-300 rounded-sm bg-white text-black",
            }),
        }
        labels = {
            "email": _("Email"),
        }