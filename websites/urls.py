from django.conf.urls import include, url
from django.views.generic import TemplateView

from dashboard.views import WebsiteCreate

urlpatterns = [
    url(r'^(?P<site_id>[0-9]+)/$', TemplateView.as_view(template_name="websites/homepage.html"), name="site_homepage"),
]
