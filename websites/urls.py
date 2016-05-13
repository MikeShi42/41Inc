from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^(?P<site_id>[0-9]+)/$', TemplateView.as_view(template_name="websites/homepage.html"), name="site_homepage"),
    url(r'^(?P<site_id>[0-9]+)/videos/', include('videos.urls', namespace='videos')),
]
