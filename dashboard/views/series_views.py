from account.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.views.generic import FormView

from series.forms import SeriesForm
from series.models import Series 


class SeriesCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'dashboard/series/createSeries.html'
    form_class = SeriesForm
    success_message = "%(title) was created successfully"
    sucess_url = '/dashboard/series/create'
