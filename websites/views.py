import account.views
import stripe
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

from fourtyone import settings
from websites.mixins import PremiumEnabledMixin
import websites.forms
from series.models import Series
from subscriptions.models import Settings as SubscriptionSettings


class SubscribeView(PremiumEnabledMixin, TemplateView):
    template_name = 'websites/payments/subscribe.html'

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)

        # Get current site
        current_site = get_current_site(self.request)

        # Get prices
        site = SubscriptionSettings.objects.get(pk=current_site.id)

        context['price_month'] = site.price_month
        context['price_year'] = site.price_year

        return context

    def post(self, request, *args, **kwargs):
        # Import API key
        stripe.api_key = settings.STRIPE_CLIENT_SECRET

        # Get token from request
        token = request.POST['token']

        # Create customer and subscribe to plan
        customer = stripe.Customer.create(
            source=token,
            plan=settings.PLAN_ID_MONTHLY
        )

        return HttpResponse(customer)

class WebsiteSignupView(account.views.SignupView):
    form_class = websites.forms.SignupForm

    def after_signup(self, form):
        # Update first/last name
        self.created_user.first_name = form.cleaned_data["first_name"]
        self.created_user.last_name = form.cleaned_data["last_name"]
        self.created_user.save()

        # Create profile
        self.create_profile(form)

        super(WebsiteSignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.profile
        profile.company = form.cleaned_data["company"]
        profile.site = get_current_site(self.request)
        profile.save()

    def login_user(self):
        user = auth.authenticate(request = self.request, **self.user_credentials())
        auth.login(self.request, user)
        self.request.session.set_expiry(0)

    def get_form_kwargs(self):
        kw = super(WebsiteSignupView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw


def site_homepage(request):
    series_for_site = Series.objects.all()
    context = {'series_for_site': series_for_site}
    return render(request, 'websites/homepage.html',context)
