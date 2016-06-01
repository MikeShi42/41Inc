from account.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.utils import timezone
from django.db.models import Sum, Avg

from django.views.generic import TemplateView

from dashboard.mixins import WebsiteCreatedMixin
from series.models import Series
from videos.models import Video
from subscriptions.models import Subscription


class DashboardView(LoginRequiredMixin, WebsiteCreatedMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user

        # Get site ID if available
        site_id = self.kwargs.get('website_id')

        # Get oldest site if not explicitly set
        if site_id is None:
            site = Site.objects.filter(info__creator=self.request.user).order_by('id')[0]
        # Otherwise we can get the site based off the URL
        else:
            site = Site.objects.get(pk=site_id)

        # Need to pass more data with each series, so making a dict
        raw_series = site.series.all()
        series = []
        for rs in raw_series:
            s = {
                'id': rs.id,
                'views': self.get_series_views(rs.id) or 0,
                'rating': self.get_series_rating(rs.id) or 0.0,
                'title': rs.title
            }
            series.append(s)
        total_views = self.get_view_count(site) or 0
        total_rating = self.get_site_rating(site) or 0.0
        total_subscribers = self.get_subscriber_count(site) or 0
        context = {
            'user': user,
            'series': series,
            'views': total_views,
            'subscribers': total_subscribers,
            'rating': total_rating,
            'site': site
        }

        return context

    def get_series_views(self, series_id):
        return Video.objects.filter(series=series_id).aggregate(Sum('views'))['views__sum']

    def get_series_rating(self, series_id):
        return Video.objects.filter(series=series_id).aggregate(Avg('rating'))['rating__avg']

    def get_view_count(self, site):
        return Video.objects.filter(site=site).aggregate(Sum('views'))['views__sum']

    def get_subscriber_count(self, site):
        return Subscription.objects.filter(site=site, active_until__gt=timezone.now()).count()

    def get_site_rating(self, site):
        return Video.objects.filter(site=site).aggregate(Avg('rating'))['rating__avg']
