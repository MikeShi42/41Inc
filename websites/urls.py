from django.conf.urls import include, url
from django.views.generic import TemplateView
import websites.views
import account.urls
import users.views

from dashboard.views import WebsiteCreate

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="websites/homepage.html"), name="home"),
    url(r"^signup/$", websites.views.WebsiteSignupView.as_view(), name="account_signup"),
    url(r"^login/$", users.views.LoginView.as_view(), name="account_login"),
    # url(r"^account/", include("users.urls")),
]

urlpatterns += account.urls.urlpatterns
