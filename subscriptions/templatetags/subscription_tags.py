from django import template
from django.contrib.sites.shortcuts import get_current_site
from subscriptions.models import Settings as SubscriptionSettings

register = template.Library()


@register.assignment_tag
def is_site_premium(request):
    return SubscriptionSettings.objects.get(pk=get_current_site(request)).premium_enabled
