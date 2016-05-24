from django import forms
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth

import account.forms
import users.forms
from subscriptions.models import Settings as SubscriptionSettings

import fourtyone.validators as f_validators


class WebsiteForm(forms.Form):
    name = forms.CharField()
    domain = forms.CharField(validators=[f_validators.validate_domain_name])
    description = forms.CharField(widget=forms.Textarea())

    def clean_domain(self):
        domain = self.cleaned_data['domain']
        if Site.objects.filter(domain=domain).count() > 0:
            raise ValidationError('This domain is already in use.')
        return domain


class PaymentSettingsForm(forms.ModelForm):

    class Meta:
        model = SubscriptionSettings
        fields = ['premium_enabled', 'price_month', 'price_year']


class SignupForm(users.forms.SignupForm):
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

