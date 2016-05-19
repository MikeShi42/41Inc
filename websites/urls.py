from django.conf.urls import include, url
from django.views.generic import TemplateView

from dashboard.views import WebsiteCreate
from websites.views import SubscribeView

urlpatterns = [
    url(r'^(?P<site_id>[0-9]+)/$', TemplateView.as_view(template_name="websites/homepage.html"), name="site_homepage"),
    url(r'^(?P<site_id>[0-9]+)/videos/(?P<video_id>[0-9]+)$', TemplateView.as_view(template_name="websites/videos/view.html"), name="site_video"),
    url(r'^(?P<site_id>[0-9]+)/subscribe/$', SubscribeView.as_view(), name="site_subscribe"),
]
