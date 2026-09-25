"""Filtres de template liés aux fichiers média.

Ils évitent d'afficher des images cassées lorsqu'un enregistrement pointe
vers un fichier qui n'existe plus (ou qui n'a jamais été téléversé).
"""

from django import template

register = template.Library()


@register.filter(name="file_exists")
def file_exists(field):
    """Vrai si le champ fichier est renseigné ET présent sur le disque."""
    if not field:
        return False
    name = getattr(field, "name", "")
    if not name:
        return False
    try:
        return field.storage.exists(name)
    except Exception:
        return False
