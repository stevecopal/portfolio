from django.views.generic import ListView, DetailView
from django.db.models import Q
from portfolio.models import Project, Technology, SiteSettings, Testimonial


class ProjectsView(ListView):
    """
    Vue pour afficher la liste complète des projets.
    - **Pagination** : 6 projets par page
    - **Filtrage** : Par technologie ou projets mis en avant
    - **Optimisation** : Utilisation de `prefetch_related` pour les technologies
    """
    template_name = "pages/projects.html"
    model = Project
    context_object_name = "projects"
    paginate_by = 6

    def get_queryset(self):
        """Filtrage des projets par technologie ou statut."""
        queryset = (
            Project.objects
            .filter(is_published=True)
            .prefetch_related("technologies", "images")
            
            .order_by("-project_date")
        )
        
        # Filtre par technologie
        tech_slug = self.request.GET.get("tech")
        if tech_slug:
            queryset = queryset.filter(technologies__slug=tech_slug)
        
        # Filtre par statut (featured, etc.)
        filter_type = self.request.GET.get("filter")
        if filter_type == "featured":
            queryset = queryset.filter(is_featured=True)
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires pour le template."""
        context = super().get_context_data(**kwargs)
        
        # Données globales
        context["site_settings"] = SiteSettings.objects.first()
        context["technologies"] = Technology.objects.order_by("display_order")
        
        # Témoignages pour la section CTA
        context["testimonials"] = Testimonial.objects.filter(is_active=True, is_featured=True).order_by("?")[:2]
        
        # Filtre actif
        context["current_filter"] = self.request.GET.get("filter", "all")
        context["current_tech"] = self.request.GET.get("tech", "")
        
        return context


class ProjectDetailView(DetailView):
    """
    Vue pour afficher les détails d’un projet.
    - **Optimisation** : Utilisation de `prefetch_related` pour les technologies et images
    - **Projets associés** : Basés sur les technologies communes
    """
    template_name = "projects/project_detail.html"
    model = Project
    context_object_name = "project"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        """Optimisation des requêtes pour le détail d'un projet."""
        return (
            Project.objects
            .prefetch_related("technologies", "images")
            .filter(is_published=True)
        )

    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires pour le template."""
        context = super().get_context_data(**kwargs)
        project = self.object
        
        # Données globales
        context["site_settings"] = SiteSettings.objects.first()
        
        # Projets associés (mêmes technologies)
        context["related_projects"] = (
            Project.objects
            .filter(
                is_published=True,
                technologies__in=project.technologies.all()
            )
            .exclude(id=project.id)
            .distinct()
            .prefetch_related("technologies", "images")
            .order_by("?")[:3]
        )
        
        # Autres projets (pour la section "You may also like")
        context["other_projects"] = (
            Project.objects
            .filter(is_published=True)
            .exclude(id=project.id)
            .prefetch_related("technologies")
            .order_by("-project_date")[:4]
        )
        
        return context


# Expose les vues pour les URLs
projects_view = ProjectsView.as_view()
project_detail_view = ProjectDetailView.as_view()