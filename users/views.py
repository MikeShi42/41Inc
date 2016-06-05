import account.views
from django.contrib.auth.mixins import LoginRequiredMixin
from account.utils import default_redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import UpdateView

import users.forms
from fourtyone import settings


class SignupView(account.views.SignupView):
    form_class = users.forms.SignupForm

    def after_signup(self, form):
        # Update first/last name
        self.created_user.first_name = form.cleaned_data["first_name"]
        self.created_user.last_name = form.cleaned_data["last_name"]
        self.created_user.save()

        # Create profile
        self.create_profile(form)

        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.profile
        profile.company = form.cleaned_data["company"]
        profile.site = get_current_site(self.request)
        profile.save()

    def login_user(self):
        user = auth.authenticate(request=self.request, **self.user_credentials())
        auth.login(self.request, user)
        self.request.session.set_expiry(0)

    def get_form_kwargs(self):
        kw = super(SignupView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            if get_current_site(self.request).id == settings.ACCOUNT_ROOT_SITE_ID:
                fallback_url = settings.ACCOUNT_ROOT_SIGNUP_REDIRECT_URL
            else:
                fallback_url = settings.ACCOUNT_CONSUMER_SIGNUP_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


class LoginView(account.views.LoginView):
    form_class = users.forms.LoginUsernameForm

    def get_form_kwargs(self):
        kw = super(LoginView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw


class AccountUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = User
    fields = ['email']
    template_name = 'websites/users/update.html'

    success_url = '/'

    success_message = 'Updated account successfully!'

    def get_object(self, queryset=None):
        return self.request.user

