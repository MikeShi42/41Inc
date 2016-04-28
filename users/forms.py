from django import forms
from django.utils.translation import ugettext_lazy as _

import account.forms


class SignupForm(account.forms.SignupForm):
    company = forms.CharField(
        label=_("Company (Optional)"),
        widget=forms.TextInput(),
        required=False
    )
