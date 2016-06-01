from django import forms
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from series.models import Series

class SeriesForm(forms.ModelForm):

    class Meta:
        model = Series 
        exclude = ['creator', 'site', 'thumbnail']
