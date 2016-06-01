from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from subscriptions.models import Settings, Subscription


class PremiumEnabledMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        site = get_current_site(self.request)
        settings = Settings.objects.get(pk=site.id)

        if settings.premium_enabled:
            return super(PremiumEnabledMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(self.redirect_to_homepage())

    def redirect_to_homepage(self):
        return reverse('home')

class SubscriptionMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SubscriptionMixin, self).get_context_data(**kwargs)

        # Check current subscription
        # TODO: clean this up because it's kind of ugly
        try:
            subscription = Subscription.objects.get(user=self.request.user)
            if subscription.active_until > timezone.now():
                context['subscribed'] = True
            else:
                context['subscribed'] = False
        except Subscription.DoesNotExist:
            context['subscribed'] = False

        return context
