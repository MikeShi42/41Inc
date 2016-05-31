# Create your views here.
import json

from account.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core import signing
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, UpdateView

from dashboard.oauth2 import stripe_connect_service
from subscriptions.models import Settings as SubscriptionSettings
from subscriptions.forms import SubscriptionSettingsForm
from subscriptions.plans import setup as setup_plans
from websites.forms import WebsiteForm
from websites.models import Info

STRIPE_STATE_SALT = 'fourtyone.stripe'


class WebsiteCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'dashboard/websites/create.html'
    form_class = WebsiteForm
    success_message = "%(name)s was created successfully"
    success_url = '/dashboard/websites/create'

    def form_valid(self, form):
        site = self.create_site(form)
        self.create_info(form, site, self.request.user)
        self.create_pay_settings(site)
        return super(WebsiteCreate, self).form_valid(form)

    def create_site(self, form):
        site = Site(name=form.cleaned_data["name"], domain=form.cleaned_data["domain"])
        site.save()
        return site

    def create_info(self, form, site, creator):
        info = Info(site=site, description=form.cleaned_data["description"], creator=creator)
        info.save()
        return info

    def create_pay_settings(self, site):
        settings = SubscriptionSettings(site=site)
        settings.save()
        return settings


class WebsiteSettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/websites/settings/settings.html'
    model = Site
    fields = ['name', 'domain']
    success_message = "Your website was updated successfully"

    def get_success_url(self):
        return reverse('websites_settings', args=(self.kwargs['pk'],))


class WebsiteSettingsInfo(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/websites/settings/info.html'
    model = Info
    fields = ['description']
    success_message = "Your website was updated successfully"

    def get_success_url(self):
        return reverse('websites_settings_info', args=(self.kwargs['pk'],))


class PaymentSettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/websites/settings/payments.html'
    model = SubscriptionSettings
    form_class = SubscriptionSettingsForm
    success_message = "Payment settings saved!"

    def get_success_url(self):
        return reverse('payments_settings', args=(self.get_object().site_id,))

    def get_context_data(self, **kwargs):
        context = super(PaymentSettings, self).get_context_data(**kwargs)

        context['site_id'] = self.kwargs['pk']

        return context


@receiver(post_save, sender=SubscriptionSettings, dispatch_uid='update_stripe_plans')
def update_stripe(sender, instance, **kwargs):
    """
    Update Stripe plans if needed when payment settings are saved
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if instance.premium_enabled and instance.price_month != 0.00 and instance.price_year != 0.00 and instance.stripe_user_id is not None:
        setup_plans(instance.stripe_user_id, price_month=to_cents(instance.price_month),
                    price_year=to_cents(instance.price_year))


def stripe_auth(request, pk):
    # Data to pass into state
    data = {
        'user_id': request.user.id,
        'site_id': pk
    }

    # Encrypt data to pass to Stripe
    state = signing.dumps(data, salt=STRIPE_STATE_SALT)

    params = {'response_type': 'code', 'scope': 'read_write', 'state': state}
    url = stripe_connect_service.get_authorize_url(**params)
    return HttpResponseRedirect(url)


def stripe_callback(request):
    # the temporary code returned from stripe
    code = request.GET['code']

    # Data passed through from the origin
    state = signing.loads(request.GET['state'], salt=STRIPE_STATE_SALT)

    # identify what we are going to ask for from stripe
    data = {
        'grant_type': 'authorization_code',
        'code': code
    }

    # Get the access_token using the code provided
    resp = stripe_connect_service.get_raw_access_token(method='POST', data=data)

    # process the returned json object from stripe
    stripe_payload = json.loads(resp.text)

    # Get settings for updating
    settings = SubscriptionSettings.objects.get(pk=state['site_id'])

    # Update info model with credentials
    settings.stripe_user_id = stripe_payload['stripe_user_id']
    settings.stripe_public_key = stripe_payload['stripe_publishable_key']
    settings.stripe_secret_key = stripe_payload['access_token']
    settings.save()

    # Create plans if proper settings are set
    if settings.premium_enabled and settings.price_month != 0.00 and settings.price_year != 0.00:
        setup_plans(stripe_payload['stripe_user_id'], price_month=to_cents(settings.price_month),
                    price_year=to_cents(settings.price_year))

    messages.success(request, 'Stripe account successfully connected!')

    # Sample return of the access_token, please don't do this! this is
    # just an example that it does in fact return the access_token
    return HttpResponseRedirect(reverse('payments_settings', args=(state['site_id'],)))


def to_cents(amount):
    return int(amount * 100)
