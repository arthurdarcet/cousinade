# coding: utf-8
from django import forms
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template import loader
from django.utils.http import int_to_base36

from auth import Backend
from models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = (
            'title',
            'first_name',
            'last_name',
            'maiden_name',
            'email',
            'phone',
            'birth_date',
            'picture',
            'father',
            'mother',
            'info',
        )

    continue_add = forms.BooleanField(required=False, label='Ajouter une autre personne')

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Titre'
        self.fields['first_name'].label = 'Prénom'
        self.fields['last_name'].label = 'Nom'
        self.fields['maiden_name'].label = 'Nom'
        self.fields['email'].label = 'E-mail'
        self.fields['phone'].label = 'Téléphone'
        self.fields['birth_date'].label = 'Date de naissance'
        self.fields['picture'].label = 'Photo'
        self.fields['father'].label = 'Père'
        self.fields['mother'].label = 'Mère'
        self.fields['info'].label = 'Info'
        self.fields['continue_add'].initial = kwargs.get('instance') is None

    def clean_email(self):
        return self.cleaned_data['email'] or None

    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()



class AuthenticationForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    remember_me = forms.BooleanField(required=False, initial=True, label='Se souvenir de moi')

    error_messages = {
        'invalid_login': 'Veuillez entrer un email et un mot de passe valide. Les mots de passe sont sensibles à la casse.',
        'no_cookies': 'Veuillez activer les cookies dans votre navigateur',
        'inactive': 'Ce compte est désactivé. Si vous pensez qu\'il s\'agit d\'une erreur, veuillez contacter {}'.format(settings.ADMINS[0][1]),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = Backend.authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'])
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self.user = Person.objects.get(email__iexact=email)
        except Person.DoesNotExist:
            raise forms.ValidationError('Email inconnu')
        return email

    def save(self, use_https=False):
            c = {
                'email': self.user.email,
                'uid': int_to_base36(self.user.id),
                'user': self.user,
                'token': default_token_generator.make_token(self.user),
                'protocol': 'https' if use_https else 'http',
                'site_name': settings.SITE_NAME,
                'domain': settings.BASE_URL,
            }
            subject = loader.render_to_string('password_reset/email_subject.txt', c)
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string('password_reset/email_body.html', c)
            send_mail(subject, email, settings.PASSWORD_RESET_FROM, [self.user.email])
            # python -m smtpd -n -c DebuggingServer localhost:1025
            # ^ to debug

class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(label='Nouveau mot de passe', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirmation', widget=forms.PasswordInput)

    def __init__(self, old_passwd_required, user, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.old_passwd_required = old_passwd_required
        self.user = user
        if old_passwd_required:
            self.fields.insert(0, 'old_password', forms.CharField(label='Ancien mot de passe', widget=forms.PasswordInput))

    def clean(self):
        if self.old_passwd_required and not self.user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError('Ancien mot de passe incorrect')
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Les deux mots de passe entrés ne sont pas identiques')
        return self.cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password2'])
        if commit:
            self.user.save()
        return self.user
