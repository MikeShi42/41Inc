from django.conf.urls import include, url
from django.views.generic import TemplateView

from dashboard.views import WebsiteCreate, PaymentSettings, stripe_auth, stripe_callback

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="dashboard/dashboard.html"), name="dashboard"),
    url(r"^websites/", include([
        url(r"^create/$", WebsiteCreate.as_view(), name="websites_create"),
        url(r"^(?P<pk>\d+)/settings/payments/$", PaymentSettings.as_view(), name="payments_settings"),
        url(r"^(?P<pk>\d+)/settings/payments/stripe$", stripe_auth, name="payments_stripe_redirect"),
        url(r"^stripe_callback/$", stripe_callback, name="payments_stripe_callback")
    ])),
]
