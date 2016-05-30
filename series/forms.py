from django import forms
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from series.models import Series

class SeriesForm(forms.ModelForm):

    class Meta:
        model = Series 
        fields = ['title', 'description']

    def clean_series(self):
        series_title = self.cleaned_data['title']
        q = Site.objects.filter(title=series_title)
        if q.exists():
        #Series.objects.filter(title=series_title).count() > 0:
            raise form.ValidationError(_('This series title is already used.'))
        return series_title
