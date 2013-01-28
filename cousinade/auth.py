# Parts of this file are copied from the Django project
# The original license and disclamer can be found here:
# https://raw.github.com/django/django/master/LICENSE
from re import compile

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.utils.functional import SimpleLazyObject
from django.shortcuts import redirect

from models import Person


EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
EXEMPT_URLS+= [compile(expr.lstrip('/')) for expr in settings.LOGIN_EXEMPT_URLS]

class Backend(object):
    @staticmethod
    def authenticate(email=None, password=None):
        try:
            user = Person.objects.get(email__iexact=email)
            if user.check_password(password):
                return user
        except Person.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return None

    @staticmethod
    def login(request, user):
        if user is None:
            user = request.user
        if SESSION_KEY in request.session:
            if request.session[SESSION_KEY] != user.pk:
                request.session.flush()
        else:
            request.session.cycle_key()
        request.session[SESSION_KEY] = user.pk
        request.user = user

    @staticmethod
    def logout(request):
        request.session.flush()
        request.user = None


class AuthenticationMiddleware(object):
    def process_request(self, request):
        try:
            user_id = request.session[SESSION_KEY]
            request.user = Backend.get_user(user_id)
        except KeyError:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
            request.user = None
