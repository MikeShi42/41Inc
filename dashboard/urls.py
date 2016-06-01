from django.conf.urls import include, url

from dashboard.views import (
    SeriesView,
    SeriesEdit,
    SeriesDelete,
    WebsiteCreate,
    WebsiteSettings,
    WebsiteSettingsInfo,
    SeriesCreate,
    VideoCreate,
    DashboardView,
    PaymentSettings,
    stripe_auth,
    stripe_callback,
    VideoDelete)

urlpatterns = [
    # url(r"^$", TemplateView.as_view(template_name="dashboard/dashboard.html"), name="dashboard"),

    url(r"^$", DashboardView.as_view(), name="dashboard"),

    # /websites/
    url(r"^websites/", include([

        # /websites/{website_id}
        url(r"^(?P<website_id>[0-9]+)/$", DashboardView.as_view(), name="websites_dashboard"),

        # /websites/create
        url(r"^create/$", WebsiteCreate.as_view(), name="websites_create"),

        # /websites/{website_id}/videos
        url(r'^(?P<website_id>[0-9]+)/videos/', include([

            # /websites/{website_id}/videos/create
            url(r'^create/$', VideoCreate.as_view(), name='create'),

            # /websites/{website_id}/videos/delete
            url(r'^(?P<pk>[0-9]+)/delete/$', VideoDelete.as_view(), name='delete')

        ], namespace='videos', app_name='videos')),

        # /websites/{website_id}/series
        url(r'^(?P<website_id>[0-9]+)/series/', include([

            # /websites/{website_id}/series/{series_id}
            url(r'^(?P<series_id>[0-9]+)$', SeriesView.as_view(), name='view'),

            # /websites/{website_id}/series/{series_id}/edit
            url(r'^(?P<pk>[0-9]+)/edit$', SeriesEdit.as_view(), name='edit'),

            # /websites/{website_id}/series/{series_id}/delete
            url(r'^(?P<pk>[0-9]+)/delete$', SeriesDelete.as_view(), name='delete'),

        ], namespace='series', app_name='series')),

        url(r'^(?P<pk>[0-9]+)/settings/', include([
            url(r"^$", WebsiteSettings.as_view(), name="websites_settings"),
            url(r"^info/$", WebsiteSettingsInfo.as_view(), name="websites_settings_info"),
            url(r"^payments/$", PaymentSettings.as_view(), name="payments_settings"),
            url(r"^payments/stripe$", stripe_auth, name="payments_stripe_redirect"),
        ])),

        url(r"^stripe_callback/$", stripe_callback, name="payments_stripe_callback")
    ])),
    url(r"^series/", include([
        url(r"^create/$", SeriesCreate.as_view(), name="series_create"),
    ])),
]
