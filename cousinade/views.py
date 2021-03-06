# coding: utf-8
from collections import defaultdict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.http import base36_to_int
from django.views.decorators.debug import sensitive_post_parameters

from .auth import Backend
from .forms import PersonForm, AuthenticationForm, PasswordResetForm, PasswordResetRequestForm
from .models import Person


def index(request):
    return render(request, 'index.html', {'objects': Person.objects.all()})

def tree(request):
    """Support multiple partners by duplicating the common parent"""
    def childs(p, h):
        ret = []
        for c in Person.objects.children(p,h):
            has_childs = False
            for cp in c.partners():
                has_childs = True
                ret.append((c,cp,childs(c,cp)))
            if not has_childs:
                ret.append((c,None,[]))
        return ret

    tree = []
    roots = set()
    for p in Person.objects.filter(mother=None, father=None):
        for h in p.partners():
            if h is None or (h.mother is None and h.father is None and p.id > h.id):
                tree.append((p,h,childs(p,h)))
    return render(request, 'tree.html', {'objects': tree})

def edit(request, pk=None):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        person = None

    form = PersonForm(instance=person)
    if request.POST:
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification effectuée' if person else 'Ajout effectué')
            return redirect('cousinade.views.edit' if form.cleaned_data.get('continue_add') else 'cousinade.views.index')

    return render(request, 'form.html', {'form': form, 'submit': 'Sauvegarder'})

@sensitive_post_parameters()
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            Backend.login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(settings.SESSION_EXPIRE)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    return render(request, 'login.html', {'form': form, 'submit': 'Se connecter'})

def logout(request):
    Backend.logout(request)
    messages.success(request, 'Déconnexion effectuée')
    return redirect(settings.LOGOUT_REDIRECT_URL)

def request_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            form.save(use_https=request.is_secure())
            messages.success(request, 'Un email vous a été envoyé pour réinitialiser votre mot de passe')
            return redirect('/')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'form.html', {'form': form, 'submit': 'Envoyer'})

@sensitive_post_parameters()
def do_password_reset(request, uidb36=None, token=None):
    try:
        uid_int = base36_to_int(uidb36)
        user = Person.objects.get(pk=uid_int)
    except (TypeError, ValueError, OverflowError, Person.DoesNotExist):
        user = None

    old_password_required = user is None or not default_token_generator.check_token(user, token)
    if old_password_required:
        if request.user:
            user = request.user
        else:
            raise Http404

    if request.method == 'POST':
        form = PasswordResetForm(old_password_required, user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre mot de passe a été réinitialisé')
            return redirect('/')
    else:
        form = PasswordResetForm(old_password_required, None)

    return render(request, 'form.html', {'form': form, 'submit': 'Sauvegarder'})
