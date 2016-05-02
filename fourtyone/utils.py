from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

# Pass in the two views main and other. Main will be a fourtyone inc view and other will be a client page view.

# Ex: url(r"^$", site_dispatch(
#       TemplateView.as_view(template_name="homepage.html"),        # Fourtyone Inc View
#       TemplateView.as_view(template_name="userhomepage.html")     # DjangoDragon, etc. View
#   ), name="home"),

def site_dispatch(main, other):
    def dispatch(request, *args, **kargs):
        current_site = get_current_site(request)
        if (current_site.domain == settings.ROOT_HOST):
            return main(request, *args, **kargs)
        else:
            return other(request, *args, **kargs)
    return dispatch