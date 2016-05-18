from django.conf.urls import include, url
from django.views.generic import TemplateView

from dashboard.views import WebsiteCreate, PaymentSettings

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="dashboard/dashboard.html"), name="dashboard"),
    url(r"^websites/", include([
        url(r"^create/$", WebsiteCreate.as_view(), name="websites_create"),
        url(r"^(?P<pk>\d+)/settings/payments/$", PaymentSettings.as_view(), name="payments_settings")
    ])),
]
