from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site


def site_processor(request):
    return {'current_site': Site.objects.get_current(request)}


def main_bg_color_processor(request):
    return {'main_bg_color': get_current_site(request).info.main_bg_color}


def main_color_processor(request):
    return {'main_color': get_current_site(request).info.main_color}
