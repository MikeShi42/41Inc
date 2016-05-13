from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from utils import site_dispatch

urlpatterns = [
    url(r"^$", site_dispatch(
        TemplateView.as_view(template_name="homepage.html"),
        TemplateView.as_view(template_name="userhomepage.html")
    ), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("users.urls")),
    url(r"^dashboard/", include("dashboard.urls")),
    url(r"^sites/", include("websites.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
