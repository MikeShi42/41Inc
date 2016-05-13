from django.conf.urls import include, url
from django.views.generic import TemplateView

from dashboard.views import WebsiteCreate

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="websites/homepage.html"), name="home"),
    url(r"^account/", include("users.urls")),
]
