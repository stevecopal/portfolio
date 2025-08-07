from django.shortcuts import redirect, render
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Avis, Profil, Projet, Article, APropos, Message
from .forms import ContactForm, LoginForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout
from django.contrib import messages


# Create your views here.

class HomeView(TemplateView):
    template_name = 'monportfolio/home.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = _("Mon Portfolio")
        context['profil'] = Profil.objects.first()  # Supposons un seul profil
        context['projets'] = Projet.objects.all()[:6]  # Récupère les 6 premiers projets
        context['articles'] = Article.objects.all()[:6]  # Récupère les 6 premiers articles
        context['form'] = self.form_class()  # Ajoute le formulaire au contexte
        context['a_propos'] = APropos.objects.first()
        return context

class ProfilView(DetailView):
    model = Profil
    template_name = 'monportfolio/profil.html'
    context_object_name = 'profil'

    def get_object(self):
        return Profil.objects.first()  # Supposons un seul profil

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['a_propos'] = APropos.objects.first()
        context['projets'] = Projet.objects.all()[:6] 
        context['titre'] = _("Mon Profil")
        return context

class ProjetListView(ListView):
    model = Projet
    template_name = 'monportfolio/projet_list.html'
    context_object_name = 'projets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = _("Mes Projets")
        return context

class ProjetDetailView(DetailView):
    model = Projet
    template_name = 'monportfolio/projet_detail.html'
    context_object_name = 'projet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ArticleListView(ListView):
    model = Article
    template_name = 'monportfolio/article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Mes Articles")
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'monportfolio/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avis'] = self.object.avis.filter()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = request.POST.get('name')
        content = request.POST.get('contenu')
        note = request.POST.get('note')
        if content:
            Avis.objects.create(
                article=self.object,
                auteur=name,
                contenu=content,
                note=note,
                
            )
            messages.success(request, "Votre commentaire a été soumis et est en attente de modération.")
        else:
            messages.error(request, "Le commentaire ne peut pas être vide.")
        return redirect(reverse('monportfolio:article_detail', kwargs={'pk': self.object.pk}))

class AProposView(DetailView):
    model = APropos
    template_name = 'monportfolio/a_propos.html'
    context_object_name = 'a_propos'

    def get_object(self):
        return APropos.objects.first()  # Supposons une seule page À propos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = _("À Propos")
        return context

class ContactView(FormView):
    template_name = 'monportfolio/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('monportfolio:contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = _("Contact")
        context['profil'] = Profil.objects.first()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ProjetListAPI(ListView):
    model = Projet

    def get(self, request, *args, **kwargs):
        projets = self.get_queryset()
        data = [
            {
                'id': str(projet.id),
                'titre': projet.titre,
                'description': projet.description,
                'image': projet.image.url if projet.image else '',
                'url': projet.url if projet.url else '',
                'categorie': projet.categorie,
            }
            for projet in projets
        ]
        return JsonResponse({'projets': data})

class ArticleListAPI(ListView):
    model = Article

    def get(self, request, *args, **kwargs):
        articles = self.get_queryset()
        data = [
            {
                'id': str(article.id),
                'titre': article.titre,
                'contenu': article.contenu[:200] + '...' if len(article.contenu) > 200 else article.contenu,
                'image': article.image.url if article.image else '',
                'categorie': article.categorie.nom if article.categorie else '',
            }
            for article in articles
        ]
        return JsonResponse({'articles': data})

class LoginView(LoginView):
    template_name = 'monportfolio/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = _("Connexion")
        return context
    
class CustomLogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('monportfolio:home'))
    
    
class ProjetListView(ListView):
    model = Projet
    template_name = 'monportfolio/projet_list.html'
    context_object_name = 'projets'
    paginate_by = 5  # 5 projets par page
    
    
from django.shortcuts import render

def portfolio(request):
    """
    Affiche la page principale avec toutes les sections (scroll).
    """
    return render(request, 'affiche.html')
