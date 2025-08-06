from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Message
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['nom', 'email', 'message']
        labels = {
            'nom': _("Nom"),
            'email': _("Email"),
            'message': _("Message"),
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'message': forms.Textarea(attrs={'class': 'form-input w-full p-2 border rounded', 'rows': 5}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Nom d'utilisateur"),
        widget=forms.TextInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
    )

    class Meta:
        fields = ['username', 'password']