from django.shortcuts import render
import account.forms
import account.views
import users.forms


class LoginView(account.views.LoginView):
    form_class = account.forms.LoginEmailForm


class SignupView(account.views.SignupView):
    form_class = users.forms.SignupForm
