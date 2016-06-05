import account.urls
from django.conf.urls import include, url

import users.views
import websites.views
from websites.views import HomeView, SubscribeView, SeriesDetailView, CustomizeView, SeriesView, VideoDetailView, \
    detail, \
    VideoIndexView

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

    ], namespace='series')),

    url(r'^api/', include([
        # /api/videos
        url(r'^videos/', include([
            # /api/videos/{video_id}
            url(r'^(?P<video_id>[0-9]+)/$', detail, name="detail"),

        ], namespace='videos'))
    ], namespace='api')),

    # url(r"^account/", include("users.urls")),
    url(r'^subscribe/$', SubscribeView.as_view(), name="site_subscribe"),

    # customization
    url(r'^customize/', CustomizeView.as_view(), name="customize"),

    url(r'^series/$', SeriesView.as_view(), name="series_browse"),
]

urlpatterns += account.urls.urlpatterns
