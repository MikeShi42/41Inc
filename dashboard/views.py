# Create your views here.
import json

from account.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core import signing
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, UpdateView

from dashboard.oauth2 import stripe_connect_service
from websites.forms import WebsiteForm, PaymentSettingsForm
from websites.models import Info

STRIPE_STATE_SALT = 'fourtyone.stripe'


class WebsiteCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'dashboard/websites/create.html'
    form_class = WebsiteForm
    success_message = "%(name)s was created successfully"
    success_url = '/dashboard/websites/create'

    def form_valid(self, form):
        self.create_site(form)
        self.create_info(form)
        return super(WebsiteCreate, self).form_valid(form)

    def create_site(self, form):
        site = Site(name=form.cleaned_data["name"], domain=form.cleaned_data["domain"])
        site.save()
        return site

    def create_info(self, form):
        info = Info(description=form.cleaned_data["description"])
        info.save()
        return info


class PaymentSettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/websites/settings/payments.html'
    model = Info
    form_class = PaymentSettingsForm
    success_message = "Payment settings saved!"

    def get_success_url(self):
        return reverse('payments_settings', args=(self.get_object().site_id,))


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

    # Get Info model for updating
    site = Info.objects.get(pk=state['site_id'])

    # Update info model with credentials
    site.stripe_user_id = stripe_payload['stripe_user_id']
    site.stripe_public_key = stripe_payload['stripe_publishable_key']
    site.stripe_secret_key = stripe_payload['access_token']
    site.save()

    messages.success(request, 'Stripe account successfully connected!')

    # Sample return of the access_token, please don't do this! this is
    # just an example that it does in fact return the access_token
    return HttpResponseRedirect(reverse('payments_settings', args=(state['site_id'],)))
