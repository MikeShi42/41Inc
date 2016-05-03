import account.urls
from django.conf.urls import include, url
import users.views

urlpatterns = [
    url(r"^signup/$", users.views.SignupView.as_view(), name="account_signup"),
]

urlpatterns += account.urls.urlpatterns
