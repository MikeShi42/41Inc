from django.views.generic.list import ListView
from django.contrib.sites.models import Site
from series.models import Series
from videos.models import Listing, Video

class SeriesView(ListView):

    template_name = 'dashboard/series/index.html'

    def get_context_data(self, **kwargs):
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs['website_id']
        context['series_id'] = self.kwargs['series_id']

        site = Site.objects.get(pk=self.kwargs['website_id'])
        series = next(Series.objects.filter(site=site, id=self.kwargs['series_id']).iterator())
        context['series'] = series

        return context

    def get_queryset(self):
        """Gets videos belonging to current site and logged in user."""
        # check for site valid
        listings = Listing.objects.filter(series=self.kwargs['series_id'])
        videos = [listing.video for listing in listings]
        return videos
