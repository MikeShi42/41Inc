from django import forms
from django.utils.translation import ugettext_lazy as _

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
