import account.urls
from django.conf.urls import include, url
import users
from users.views import LoginView

urlpatterns = [
    url(r"^login/$", LoginView.as_view(), name="account_login"),  # Overriding the accounts login form
    url(r"^signup/$", users.views.SignupView.as_view(), name="account_signup"),
]

urlpatterns += account.urls.urlpatterns
