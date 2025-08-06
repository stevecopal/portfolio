from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Categorie, Profil, ReseauSocial, Projet, Article, Avis, APropos, Competence, Message

# Inline pour gérer les réseaux sociaux dans le formulaire Profil
class ReseauSocialInline(admin.TabularInline):
    model = ReseauSocial
    extra = 1
    verbose_name = _("Réseau social")
    verbose_name_plural = _("Réseaux sociaux")

# Inline pour gérer les compétences dans le formulaire APropos
class CompetenceInline(admin.TabularInline):
    model = Competence
    extra = 1
    verbose_name = _("Compétence")
    verbose_name_plural = _("Compétences")

# Inline pour gérer les avis dans le formulaire Article
class AvisInline(admin.TabularInline):
    model = Avis
    extra = 1
    verbose_name = _("Avis")
    verbose_name_plural = _("Avis")

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'id']
    search_fields = ['nom']
    list_filter = ['nom']
    ordering = ['nom']

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['nom', 'titre', 'email', 'date_creation']
    search_fields = ['nom', 'titre', 'email']
    list_filter = ['date_creation', 'date_modification']
    inlines = [ReseauSocialInline]
    fieldsets = (
        (None, {'fields': ('nom', 'titre', 'description', 'email', 'telephone', 'localisation')}),
        ('Médias', {'fields': ('photo', 'cv')}),
    )

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'date_creation']
    search_fields = ['titre', 'description', 'categorie']
    list_filter = ['categorie', 'date_creation', 'date_modification']
    list_editable = ['categorie']
    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'image', 'url', 'categorie')
        }),
        
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'date_creation']
    search_fields = ['titre', 'contenu']
    list_filter = ['categorie', 'date_creation', 'date_modification']
    inlines = [AvisInline]
    fieldsets = (
        (None, {
            'fields': ('titre', 'contenu', 'image', 'categorie')
        }),

    )

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ['auteur', 'article', 'note', 'date_creation']
    search_fields = ['auteur', 'contenu', 'article__titre']
    list_filter = ['note', 'date_creation', 'article']
    fieldsets = (
        (None, {
            'fields': ('article', 'auteur', 'contenu', 'note')
        }),
        
    )

@admin.register(APropos)
class AProposAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_creation']
    search_fields = ['contenu']
    inlines = [CompetenceInline]
    fieldsets = (
        (None, {
            'fields': ('contenu',)
        }),
        
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'date_envoi']
    search_fields = ['nom', 'email', 'message']
    list_filter = ['date_envoi']
    fieldsets = (
        (None, {
            'fields': ('nom', 'email', 'message', 'date_envoi')
        }),
        
    )

# Enregistrement explicite pour ReseauSocial et Competence (si nécessaire)
@admin.register(ReseauSocial)
class ReseauSocialAdmin(admin.ModelAdmin):
    list_display = ['nom', 'profil', 'url']
    search_fields = ['nom', 'url']
    list_filter = ['profil']

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'apropos']
    search_fields = ['nom']
    list_filter = ['apropos']
    
    
admin.site.site_header = _("Copal Admin")
admin.site.site_title = _("Copal Portfolio Admin Portal")
admin.site.index_title = _("Welcome to Copal Portfolio")