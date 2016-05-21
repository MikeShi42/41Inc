from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from account.utils import get_user_lookup_kwargs
from users.models import Profile
from django.contrib.sites.shortcuts import get_current_site


class UsernameSiteAuthenticationBackend(ModelBackend):

    def authenticate(self, request, **credentials):
        User = get_user_model()
        print "user:"
        print User
        current_site = get_current_site(request)
        try:
            lookup_kwargs = get_user_lookup_kwargs({
                "{username}__iexact": credentials["username"]
            })
            user = User.objects.get(**lookup_kwargs)
        except (User.DoesNotExist, KeyError):
            return None
        else:
            try:
                profile = Profile.objects.get(user=user.id)
                print "profile:"
                print profile
                if user.check_password(credentials["password"]) and profile.site_id == current_site.id:
                    return user
            except KeyError:
                return None