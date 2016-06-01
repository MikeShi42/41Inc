from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView
from django.views.generic import FormView

from series.forms import SeriesForm 
from series.models import Series

class SeriesCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    model = Series
    template_name = 'dashboard/series/createSeries.html'
    form_class = SeriesForm
    success_message = "%(title)s was created successfully"
    success_url = '/dashboard/series/create'
                
    def form_valid(self, form):
        self.create_series(form)
        return super(SeriesCreate, self).form_valid(form)
 
    def create_series(self, form):
        """Set the creator_id of the newly created series to the user that's 
        currently logged in and also fills in the title and description fields
        """        
        series =  Series(title=form.cleaned_data['title'], description=form.cleaned_data['description'], creator=self.request.user)
        series.save()
        return series 
