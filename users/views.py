from django.shortcuts import render
import account.forms
import account.views


# Create your views here.

class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm
