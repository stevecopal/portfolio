from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from portfolio.models import SiteSettings, Service
from portfolio.forms import ContactForm

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
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("portfolio:contact")
        else:
            context = self.get_context_data()
            context["form"] = form
            return render(request, self.template_name, context)

contact_view = ContactView.as_view()