from django import template

from fourtyone import settings

register = template.Library()


@register.simple_tag
def stripe_public_key():
    return settings.STRIPE_PUBLIC_KEY
