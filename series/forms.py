from django import forms

class SeriesForm(forms.Form):
        title = forms.CharField();
        description = forms.CharField(widget=forms.Textarea())
