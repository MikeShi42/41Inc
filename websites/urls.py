from django.conf.urls import include, url
from django.views.generic import TemplateView
import websites.views
import account.urls
import users.views
from websites.views import SubscribeView

urlpatterns = [
    url(r"^$", websites.views.site_homepage, name="home"),
    url(r"^signup/$", websites.views.WebsiteSignupView.as_view(), name="account_signup"),
    url(r"^login/$", users.views.LoginView.as_view(), name="account_login"),
    # url(r"^account/", include("users.urls")),
    url(r'^videos/(?P<video_id>[0-9]+)$', TemplateView.as_view(template_name="websites/videos/view.html"), name="site_video"),
    url(r'^subscribe/$', SubscribeView.as_view(), name="site_subscribe"),
    url(r'^series/$', websites.views.browse_series, name="series_browse"),
]

urlpatterns += account.urls.urlpatterns
