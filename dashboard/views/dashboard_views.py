from django.http import HttpResponse

from django.views.generic import TemplateView
from django.shortcuts import render
from websites.models import Info
from videos.models import Video
from series.models import Series
from subscriptions.models import Subscription


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self):

        user = self.request.user

        # Need to pass more data with each series, so making a dict
        raw_series = Series.objects.filter(creator_id=user.id)
        series = []
        for rs in raw_series:
            s = {
                'views': sum(v.views for v in Video.objects.filter(
                    series=rs.id,
                )),
                'rating': (sum(r.ratings for r in Video.objects.filter(
                    series=rs.id
                )) or 0.0) / 5.0,
                'title': rs.title,
                'subscribers': 1,
            }
            series.append(s)
        total_views = sum(v.views for v in Video.objects.filter(
                    creator_id=user.id
                )) or 0
        total_rating = (sum(r.ratings for r in Video.objects.filter(
                    creator_id=user.id
                )) or 0.0) / 5.0
        total_subscribers = sum(1 for s in Subscription.objects.filter(
                    user_id=user.id
                )) or 0
        context = {
            'user': user,
            'series': series,
            'websites': Info.objects.filter(creator_id=user.id),
            'views': total_views,
            'subscribers': total_subscribers,
            'rating': total_rating

        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)