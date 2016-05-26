from django import forms

class SeriesForm(forms.Form):
        series_name = forms.CharField();
        description = forms.CharField(widget=forms.Textarea())
