from django.conf.urls import include, url
from websites.views import WebsiteView

urlpatterns = [
    url(r"^create/$", WebsiteView.as_view(), name="websites_create"),
]
