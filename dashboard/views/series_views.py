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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView
from django.views.generic.list import ListView

from series.forms import SeriesForm 
from series.models import Series

class SeriesCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Series
    template_name = 'dashboard/series/createSeries.html'
    form_class = SeriesForm
    success_message = "%(title)s was created successfully"
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        self.create_series(form)
        return super(SeriesCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SeriesCreate, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs['website_id']
        return context

 
    def create_series(self, form):
        """Set the creator_id of the newly created series to the user that's 
        currently logged in and also fills in the title and description fields
        """        
        curr_site = get_current_site(self.request)
        series = form.save(commit=False)
        series.site = Site.objects.get(pk=self.kwargs['website_id'])
        series.creator = self.request.user
        series.save()
        return series


class SeriesView(LoginRequiredMixin, ListView):

    template_name = 'dashboard/series/index.html'

    def get_context_data(self, **kwargs):
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs['website_id']
        context['series_id'] = self.kwargs['series_id']

        site = Site.objects.get(pk=self.kwargs['website_id'])
        series = next(Series.objects.filter(site=site, id=self.kwargs['series_id']).iterator())
        context['series'] = series

        return context

    def get_queryset(self):
        """Gets videos belonging to current site and logged in user."""
        # check for site valid
        listings = Listing.objects.filter(series=self.kwargs['series_id'])
        videos = [listing.video for listing in listings]
        return videos

class SeriesEdit(LoginRequiredMixin, UpdateView):
    model = Series

    fields=['title', 'description', 'thumbnail_url']

    template_name='dashboard/series/editSeries.html'

    def get_context_data(self, **kwargs):
        context = super(SeriesEdit, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs.get('website_id')
        context['pk'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse('series:view', kwargs = {
            'website_id': self.kwargs.get('website_id'),
            'series_id':self.kwargs.get('pk')
        })


class SeriesDelete(LoginRequiredMixin, DeleteView):

    model = Series

    success_url = reverse_lazy('dashboard')

    template_name = 'dashboard/series/deleteSeries.html'

    def get_context_data(self, **kwargs):
        context = super(SeriesDelete, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs.get('website_id')
        context['pk'] = self.kwargs.get('pk')
        return context
