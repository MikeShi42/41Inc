from django import template
from django.contrib.sites.models import Site

register = template.Library()


@register.assignment_tag
def get_sites(user):
    return Site.objects.filter(info__creator=user)
