from django import forms
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from series.models import Series

class SeriesForm(forms.ModelForm):

    class Meta:
        model = Series 
        fields = ['title', 'description']

    def clean_series(self):
        title = self.cleaned_data['title']
        if Series.objects.filter(title=title).count() > 0:
            raise ValidationError('This series title is already used.')
        return title
