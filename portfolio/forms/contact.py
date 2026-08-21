from django import forms
from django.utils.translation import gettext_lazy as _
from portfolio.models import ContactMessage

class ContactForm(forms.ModelForm):
    BUDGET_CHOICES = [
        ("", _("Select Budget")),
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
        ("custom", _("Custom")),
    ]

    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "email", "subject", "service", "budget", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "email": _("Email"),
            "subject": _("Subject"),
            "service": _("Service"),
            "budget": _("Budget"),
            "message": _("Message"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["budget"].choices = self.BUDGET_CHOICES
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "w-full p-3 border border-gray-300 rounded-sm bg-white text-black"})