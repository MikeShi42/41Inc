from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from account.utils import get_user_lookup_kwargs
from account.models import EmailAddress
from users.models import Profile
from account.conf import settings
import re

import account.forms


class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField(
        label=_("First Name"),
        widget=forms.TextInput()
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        widget=forms.TextInput()
    )
    company = forms.CharField(
        label=_("Company (Optional)"),
        widget=forms.TextInput(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        alnum_re = re.compile(r"^\w+$")
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)

        # TODO: Uncomment below lines when unique constraint on auth_user.username is resolved
        # ids = [user['id'] for user in qs.values()]
        # site = get_current_site(self.request)
        # prof = Profile.objects.filter(id__in=ids, site_id=site.id)

        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    # TODO: Disallow multiple emails per site
    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

# Adding on site validation
class LoginUsernameForm(account.forms.LoginUsernameForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginUsernameForm, self).__init__(*args, **kwargs)

    # Overwritten to pass request into authentication function
    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(request=self.request, **self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is inactive."))
        else:
            raise forms.ValidationError(self.authentication_fail_message)
        return self.cleaned_data
