from django import forms
from django.forms import ModelForm

from websites.models import Website


class WebsiteForm(ModelForm):
    class Meta:
        model = Website
        fields = ["name", "description", "domain"]
