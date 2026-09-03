from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from portfolio.models import SiteSettings, Service
from portfolio.forms import ContactForm


class ContactView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        context["services"] = Service.objects.filter(is_active=True).order_by(
            "display_order"
        )
        context["form"] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        
        if form.is_valid():
            data = form.cleaned_data
            service_name = data["service"].title if data["service"] else ""

            try:
                subject = f"[Portfolio] {data['first_name']} {data['last_name']} - {data['subject']}"

                context = {
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "subject": data["subject"],
                    "service": service_name,
                    "budget": dict(form.BUDGET_CHOICES).get(
                        data["budget"], data["budget"]
                    ),
                    "message": data["message"],
                    "site_settings": SiteSettings.objects.first(),
                    "now": timezone.now(),
                    "request": request,
                }

                html_message = render_to_string(
                    "emails/contact_message.html", context
                )
                text_message = strip_tags(html_message)

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],
                    reply_to=[data["email"]],
                )
                email.attach_alternative(html_message, "text/html")
                email.send()

                if is_ajax:
                    return JsonResponse({
                        "success": True,
                        "message": str(_("Thank you! Your message has been sent successfully.")),
                        "redirect": reverse("portfolio:home") + "#contact"
                    })

                messages.success(
                    request,
                    _("Thank you! Your message has been sent successfully."),
                )
                return HttpResponseRedirect(
                    reverse("portfolio:home") + "#contact"
                )

            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Email error: {e}")
                
                if is_ajax:
                    return JsonResponse({
                        "success": False,
                        "message": str(_("Sorry, there was an error sending your message. Please try again."))
                    })

                messages.error(
                    request,
                    _(
                        "Sorry, there was an error sending your message. Please try again."
                    ),
                )

        if is_ajax:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            return JsonResponse({
                "success": False,
                "message": str(_("Please correct the errors below.")),
                "errors": errors
            })

        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)


contact_view = ContactView.as_view()
