from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView, DetailView

from series.models import Series
from videos.models import Listing


class SeriesView(TemplateView):
    template_name = 'websites/series/index.html'

    def get_context_data(self, **kwargs):
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['series_for_site'] = Series.objects.filter(site=get_current_site(self.request))
        return context


class SeriesDetailView(DetailView):
    template_name = 'websites/series/detail.html'
    model = Series

    def get_context_data(self, **kwargs):
        context = super(SeriesDetailView, self).get_context_data(**kwargs)
        listings = Listing.objects.filter(series=self.kwargs['pk'])
        context['videos'] = [listing.video for listing in listings]
        return context
