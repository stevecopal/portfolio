from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils import translation


class LanguageMiddleware:
    """Gère la bascule de langue via le paramètre ``?lang=xx``.

    Le paramètre est converti en redirection ``302`` vers l'URL officielle de
    la langue (préfixe d'URL) afin de ne jamais exposer deux adresses pour un
    même contenu — ce qui pénalise le référencement (contenu dupliqué).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from URL or cookie
        language = request.GET.get("lang")
        supported = [lang[0] for lang in settings.LANGUAGES]
        if language and language in supported:
            # Important : l'URL traduite est calculée AVANT d'activer la
            # nouvelle langue, car resolve() dépend de la langue courante.
            target = translate_url(request.path, language)
            translation.activate(language)
            response = HttpResponseRedirect(target or "/")
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                language,
                max_age=365 * 24 * 60 * 60,
            )
            return response
        return self.get_response(request)
