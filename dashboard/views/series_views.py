import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.views.generic import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect 
from django.views import generic
from django.views.generic.edit import CreateView
from series.forms import SeriesForm
from series.models import Series 
from django.core.exceptions import ValidationError

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
        series =  Series(title=form.cleaned_data['title'], 
                description=form.cleaned_data['description'])
        title = form.cleaned_data['title']
        if Series.objects.filter(title=title).count() > 0:
            raise ValidationError('Title already in use')
        series.save()
        return series 
