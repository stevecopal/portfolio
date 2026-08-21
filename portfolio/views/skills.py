from django.views.generic import TemplateView, ListView
from portfolio.models import Skill, SkillCategory, SiteSettings


class SkillsView(ListView):
    """
    Vue pour afficher la liste complète des compétences.
    - **Groupées par catégorie**
    - **Triées par ordre d'affichage**
    """
    template_name = "pages/skills.html"
    model = Skill
    context_object_name = "skills"

    def get_queryset(self):
        """Récupère toutes les compétences actives, triées par catégorie et ordre d'affichage."""
        return (
            Skill.objects
            .filter(is_active=True)
            .select_related("category")
            .order_by("category__display_order", "display_order")
        )

    def get_context_data(self, **kwargs):
        """Ajoute les catégories et les paramètres du site."""
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.objects.first()
        context["skill_categories"] = SkillCategory.objects.prefetch_related("skills").order_by("display_order")
        return context


class SkillsSectionView(TemplateView):
    """
    Vue pour afficher UNIQUEMENT la section Skills (à inclure dans la homepage).
    """
    template_name = "components/skills_section.html"

    def get_context_data(self, **kwargs):
        """Récupère les compétences et catégories pour la section."""
        context = super().get_context_data(**kwargs)
        context["skill_categories"] = SkillCategory.objects.prefetch_related(
            "skills"
        ).filter(skills__is_active=True).order_by("display_order").distinct()
        context["featured_skills"] = Skill.objects.filter(is_featured=True, is_active=True).order_by("display_order")[:6]
        return context


# Expose les vues
skills_view = SkillsView.as_view()
skills_section_view = SkillsSectionView.as_view()