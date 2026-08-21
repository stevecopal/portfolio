from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from portfolio.models import SiteSettings, Service
from portfolio.forms import ContactForm
from django.utils.translation import gettext_lazy as _
class ContactView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        context["services"] = Service.objects.filter(is_active=True).order_by("display_order")
        context["form"] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Récupère les données
            data = form.cleaned_data
            service_name = data["service"].title if data["service"] else ""

            try:
                # Sujet de l'email
                subject = f"[Portfolio] {data['first_name']} {data['last_name']} - {data['subject']}"

                # Contexte pour le template email
                context = {
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "subject": data["subject"],
                    "service": service_name,
                    "budget": dict(form.BUDGET_CHOICES).get(data["budget"], data["budget"]),
                    "message": data["message"],
                    "site_settings": SiteSettings.objects.first(),
                    "now": timezone.now(),
                    "request": request,
                }

                # Render HTML
                html_message = render_to_string("emails/contact_message.html", context)
                text_message = strip_tags(html_message)

                # Crée et envoie l'email
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],  # ✅ Envoie à TON email
                    reply_to=[data["email"]]  # Pour répondre directement au client
                )
                email.attach_alternative(html_message, "text/html")
                email.send()

                messages.success(request, _("Thank you! Your message has been sent successfully."))
                return redirect("portfolio:contact")

            except Exception as e:
                messages.error(request, _("Sorry, there was an error sending your message. Please try again."))
                # Log l'erreur (optionnel)
                import logging
                logging.getLogger(__name__).error(f"Email error: {e}")

        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)

contact_view = ContactView.as_view()