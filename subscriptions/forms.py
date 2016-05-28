from django import forms

from subscriptions.models import Settings


class SubscriptionSettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ['premium_enabled', 'price_month', 'price_year']