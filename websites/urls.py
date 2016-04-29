from django.conf.urls import include, url
from websites.views import WebsiteCreate

urlpatterns = [
    url(r"^create/$", WebsiteCreate.as_view(), name="websites_create"),
]
