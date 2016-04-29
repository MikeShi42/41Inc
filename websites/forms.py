from django import forms


class WebsiteForm(forms.Form):
    name = forms.CharField()
    domain = forms.CharField()
    description = forms.CharField()
