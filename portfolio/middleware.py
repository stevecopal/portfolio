from django.utils import translation
from django.conf import settings

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from URL or cookie
        language = request.GET.get('lang')
        if language and language in [lang[0] for lang in settings.LANGUAGES]:
            translation.activate(language)
            response = self.get_response(request)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, max_age=365*24*60*60)
            return response
        return self.get_response(request)