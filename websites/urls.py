import account.urls
from django.conf.urls import include, url
from django.views.generic import ListView

import users.views
import websites.views
from dashboard.views import VideoIndexView, VideoDetailView, detail
from series.models import Series
from websites.views import HomeView, SubscribeView, SeriesDetailView

urlpatterns = [
    # Root URL for client sites /
    url(r"^$", HomeView.as_view(), name="home"),

    # Authentication URLs, /signup and /login
    url(r"^signup/$", websites.views.WebsiteSignupView.as_view(), name="account_signup"),
    url(r"^login/$", users.views.LoginView.as_view(), name="account_login"),

    # /videos
    url(r'^videos/', include([
        # /videos/
        url(r'^$', VideoIndexView.as_view(), name='index'),

        # /videos/{video_id}
        url(r'^(?P<pk>[0-9]+)/$', VideoDetailView.as_view(), name="detail"),

    ], namespace='videos')),

    # /series
    url(r'^series/', include([
        # /videos/{video_id}
        url(r'^(?P<pk>[0-9]+)/$', SeriesDetailView.as_view(), name="detail"),

    ], namespace='videos')),

    url(r'^api/', include([
        # /api/videos
        url(r'^videos/', include([
            # /api/videos/{video_id}
            url(r'^(?P<video_id>[0-9]+)/$', detail, name="detail"),

        ], namespace='videos'))
    ], namespace='api')),

    # url(r"^account/", include("users.urls")),
    url(r'^subscribe/$', SubscribeView.as_view(), name="site_subscribe"),
]

urlpatterns += account.urls.urlpatterns
