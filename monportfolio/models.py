from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
class BaseModel(models.Model):
    """
    Classe abstraite de base pour tous les modèles.
    Fournit des champs communs pour l'identifiant et les métadonnées temporelles.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name=_("Identifiant")
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de modification")
    )
    date_suppression = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name=_("Date de suppression")
    )

    class Meta:
        abstract = True
        ordering = ['-date_creation']

class Categorie(models.Model):
    """
    Modèle pour les catégories des articles.
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Nom")
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        ordering = ['nom']

class Profil(BaseModel):
    """
    Modèle pour les informations personnelles affichées dans la section Profil et Contact.
    """
    nom = models.CharField(
        max_length=200,
        verbose_name=_("Nom")
    )
    titre = models.CharField(
        max_length=200,
        verbose_name=_("Titre professionnel")
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    photo = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name=_("Photo de profil")
    )
    email = models.EmailField(
        verbose_name=_("Email")
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Téléphone")
    )
    localisation = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Localisation")
    )
    cv = models.FileField(
        upload_to='media/',
        blank=True,
        null=True,
        verbose_name=_("CV")
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _("Profil")
        verbose_name_plural = _("Profils")

class ReseauSocial(models.Model):
    """
    Modèle pour les liens vers les réseaux sociaux, liés au profil.
    """
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='reseaux_sociaux',
        verbose_name=_("Profil")
    )
    nom = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )
    url = models.URLField(
        verbose_name=_("URL")
    )
    icone = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("Icône (emoji ou code)")
    )

    def __str__(self):
        return f"{self.nom} ({self.profil.nom})"

    class Meta:
        verbose_name = _("Réseau social")
        verbose_name_plural = _("Réseaux sociaux")
        ordering = ['nom']

class Projet(BaseModel):
    """
    Modèle pour les projets affichés dans la section Projets.
    """
    titre = models.CharField(
        max_length=200,
        verbose_name=_("Titre")
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name=_("Image")
    )
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("URL du projet")
    )
    categorie = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Catégorie")
    )

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = _("Projet")
        verbose_name_plural = _("Projets")

    
class Article(BaseModel):
    """
    Modèle pour les articles affichés dans la section Articles.
    """
    titre = models.CharField(
        max_length=200,
        verbose_name=_("Titre")
    )
    contenu = RichTextField(
        verbose_name=_("Contenu")
    )
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name=_("Image")
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Catégorie")
    )

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        
   

class Avis(BaseModel):
    """
    Modèle pour les avis laissés sur les articles.
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='avis',
        verbose_name=_("Article")
    )
    auteur = models.CharField(
        max_length=200,
        verbose_name=_("Auteur")
    )
    contenu = models.TextField(
        verbose_name=_("Contenu")
    )
    note = models.IntegerField(
        verbose_name=_("Note"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def __str__(self):
        return f"Avis de {self.auteur} pour {self.article.titre}"

    class Meta:
        verbose_name = _("Avis")
        verbose_name_plural = _("Avis")
        ordering = ['-date_creation']

class APropos(BaseModel):
    """
    Modèle pour le contenu de la section À propos.
    """
    contenu = models.TextField(
        verbose_name=_("Contenu")
    )

    def __str__(self):
        return f"À propos ({self.id})"

    class Meta:
        verbose_name = _("À propos")
        verbose_name_plural = _("À propos")

class Competence(models.Model):
    """
    Modèle pour les compétences listées dans la section À propos.
    """
    apropos = models.ForeignKey(
        APropos,
        on_delete=models.CASCADE,
        related_name='competences',
        verbose_name=_("À propos")
    )
    nom = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _("Compétence")
        verbose_name_plural = _("Compétences")
        ordering = ['nom']

class Message(BaseModel):
    """
    Modèle pour les messages envoyés via le formulaire de contact.
    """
    nom = models.CharField(
        max_length=200,
        verbose_name=_("Nom")
    )
    email = models.EmailField(
        verbose_name=_("Email")
    )
    message = models.TextField(
        verbose_name=_("Message")
    )
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date d'envoi")
    )

    def __str__(self):
        return f"Message de {self.nom}"

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['-date_envoi']