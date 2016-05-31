from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from websites.models import Info


class SiteIdMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SiteIdMixin, self).get_context_data(**kwargs)
        context['site_id'] = self.kwargs['pk']
        return context


class WebsiteCreatedMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        user = self.request.user

        if Info.objects.filter(creator=user).count() > 0:
            return super(WebsiteCreatedMixin, self).dispatch(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('websites_create'))
