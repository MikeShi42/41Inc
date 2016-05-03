from django.shortcuts import render
import account.forms
import account.views
import users.forms
from django.contrib.sites.shortcuts import get_current_site


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
