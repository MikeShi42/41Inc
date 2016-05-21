from django import forms
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

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
