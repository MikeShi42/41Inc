from django.shortcuts import render
from django.http import HttpResponse

from series.models import Series
# from .models import

# Create your views here.


def site_homepage(request, site_id):
    # series_for_site = Series.objects.filter(site_id = site_id)

    series_for_site = Series.objects.all()
    context = {'series_for_site': series_for_site}
    return render(request, 'websites/homepage.html',context)
