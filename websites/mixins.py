from __future__ import unicode_literals

from account.conf import settings
from account.utils import handle_redirect_to_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from subscriptions.models import Settings


class PremiumEnabledMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        site = Settings.objects.get(pk=get_current_site(self.request).id)

        if site.premium_enabled:
            return super(PremiumEnabledMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(self.redirect_to_homepage())

    def redirect_to_homepage(self):
        return reverse('site_homepage', args=(self.kwargs['site_id'],))
