from django.conf.urls import include, url
from django.views.generic import TemplateView

from dashboard.views import WebsiteCreate, VideoCreate, VideoIndexView, PaymentSettings, stripe_auth, stripe_callback

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="dashboard/dashboard.html"), name="dashboard"),

    # /websites/
    url(r"^websites/", include([

        # /websites/create
        url(r"^create/$", WebsiteCreate.as_view(), name="websites_create"),

        # /websites/{website_id}/videos
        url(r'^(?P<website_id>[0-9]+)/videos/', include([

            # /websites/{website_id}/videos/
            url(r'^$', VideoIndexView.as_view(), name='index'),

            # /websites/{website_id}/videos/create
            url(r'^create/$', VideoCreate.as_view(), name='create')
        ], namespace='videos', app_name='videos')),

        url(r"^(?P<pk>\d+)/settings/payments/$", PaymentSettings.as_view(), name="payments_settings"),
        url(r"^(?P<pk>\d+)/settings/payments/stripe$", stripe_auth, name="payments_stripe_redirect"),
        url(r"^stripe_callback/$", stripe_callback, name="payments_stripe_callback")
    ])),
]
