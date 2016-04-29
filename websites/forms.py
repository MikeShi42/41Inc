from django import forms


class WebsiteForm(forms.Form):
    name = forms.CharField(label='Site Name', strip=True)
    description = forms.CharField(label='Description', strip=True)
    domain = forms.CharField(label='Domain', strip=True)
