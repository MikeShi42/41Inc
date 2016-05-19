from django.views.generic import TemplateView

from websites.models import Info


class SubscribeView(TemplateView):
    template_name = 'websites/payments/subscribe.html'

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)

        # Get prices
        site = Info.objects.get(pk=self.kwargs['site_id'])

        context['price_month'] = site.price_month
        context['price_year'] = site.price_year

        return context
