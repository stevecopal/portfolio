import re
from django.utils.text import slugify as django_slugify
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


def generate_slug(text, model=None, field="slug"):
    """
    Génère un slug unique pour un modèle donné.
    
    Args:
        text (str): Le texte à convertir en slug.
        model: Le modèle Django pour vérifier l'unicité.
        field (str): Le nom du champ de slug dans le modèle.
    
    Returns:
        str: Un slug unique.
    """
    # Générer le slug de base
    slug = django_slugify(text)
    
    # Si aucun modèle n'est fourni, retourner le slug de base
    if not model:
        return slug
    
    # Vérifier l'unicité du slug
    original_slug = slug
    counter = 1
    while model.objects.filter(**{field: slug}).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    return slug


def format_date(date, format="long"):
    """
    Formate une date selon un format donné.
    
    Args:
        date: La date à formater.
        format (str): Le format de sortie ('long', 'short', 'iso').
    
    Returns:
        str: La date formatée.
    """
    if not date:
        return ""
    
    if format == "long":
        return date.strftime("%B %d, %Y")
    elif format == "short":
        return date.strftime("%b %d, %Y")
    elif format == "iso":
        return date.isoformat()
    elif format == "year":
        return date.strftime("%Y")
    else:
        return date.strftime("%Y-%m-%d")


def truncate_text(text, max_length=100, suffix="..."):
    """
    Tronque un texte à une longueur maximale.
    
    Args:
        text (str): Le texte à tronquer.
        max_length (int): La longueur maximale.
        suffix (str): Le suffixe à ajouter si le texte est tronqué.
    
    Returns:
        str: Le texte tronqué.
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def get_absolute_url(obj, request=None):
    """
    Récupère l'URL absolue d'un objet.
    
    Args:
        obj: L'objet avec une méthode get_absolute_url().
        request: La requête HTTP (optionnelle).
    
    Returns:
        str: L'URL absolue.
    """
    if not obj:
        return ""
    
    if hasattr(obj, 'get_absolute_url'):
        url = obj.get_absolute_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
    return ""


def get_model_name(obj):
    """
    Récupère le nom du modèle d'un objet.
    
    Args:
        obj: L'objet Django.
    
    Returns:
        str: Le nom du modèle en minuscules.
    """
    if not obj:
        return ""
    return obj._meta.model_name.lower()


def get_reading_time(text, words_per_minute=200):
    """
    Calcule le temps de lecture estimé pour un texte.
    
    Args:
        text (str): Le texte à analyser.
        words_per_minute (int): Le nombre de mots par minute (par défaut: 200).
    
    Returns:
        int: Le temps de lecture en minutes.
    """
    if not text:
        return 0
    
    # Supprimer les balises HTML
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    # Compter les mots
    word_count = len(clean_text.split())
    
    # Calculer le temps de lecture
    reading_time = word_count / words_per_minute
    
    return max(1, int(round(reading_time)))


def get_client_ip(request):
    """
    Récupère l'adresse IP du client.
    
    Args:
        request: La requête HTTP.
    
    Returns:
        str: L'adresse IP du client.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Récupère l'agent utilisateur (User-Agent) de la requête.
    
    Args:
        request: La requête HTTP.
    
    Returns:
        str: L'agent utilisateur.
    """
    return request.META.get('HTTP_USER_AGENT', '')


def is_mobile(request):
    """
    Vérifie si la requête provient d'un appareil mobile.
    
    Args:
        request: La requête HTTP.
    
    Returns:
        bool: True si l'appareil est mobile, False sinon.
    """
    user_agent = get_user_agent(request).lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone']
    return any(keyword in user_agent for keyword in mobile_keywords)


def is_ajax(request):
    """
    Vérifie si la requête est une requête AJAX.
    
    Args:
        request: La requête HTTP.
    
    Returns:
        bool: True si la requête est AJAX, False sinon.
    """
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def get_next_url(request, default='/'):
    """
    Récupère l'URL de redirection depuis les paramètres de la requête.
    
    Args:
        request: La requête HTTP.
        default (str): L'URL par défaut si 'next' n'est pas présent.
    
    Returns:
        str: L'URL de redirection.
    """
    next_url = request.GET.get('next', default)
    return next_url if next_url else default


def validate_email(email):
    """
    Valide une adresse e-mail.
    
    Args:
        email (str): L'adresse e-mail à valider.
    
    Returns:
        bool: True si l'e-mail est valide, False sinon.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    Valide un numéro de téléphone (format international).
    
    Args:
        phone (str): Le numéro de téléphone à valider.
    
    Returns:
        bool: True si le numéro est valide, False sinon.
    """
    import re
    # Format international : + suivi de 8 à 15 chiffres
    pattern = r'^\+[1-9]\d{7,14}$'
    return re.match(pattern, phone) is not None


def sanitize_html(html):
    """
    Nettoie le HTML pour éviter les attaques XSS.
    
    Args:
        html (str): Le HTML à nettoyer.
    
    Returns:
        str: Le HTML nettoyé.
    """
    import html
    return html.escape(html)


def get_pagination_range(page_obj, max_links=5):
    """
    Génère une plage de numéros de page pour la pagination.
    
    Args:
        page_obj: L'objet Page de Django.
        max_links (int): Le nombre maximum de liens à afficher.
    
    Returns:
        list: Une liste de numéros de page à afficher.
    """
    current = page_obj.number
    total = page_obj.paginator.num_pages
    
    # Calculer la plage de pages
    start = max(1, current - max_links // 2)
    end = min(total, start + max_links - 1)
    
    if end - start + 1 < max_links:
        start = max(1, end - max_links + 1)
    
    return list(range(start, end + 1))