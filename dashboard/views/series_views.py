from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView
from django.views.generic.list import ListView

from series.forms import SeriesForm
from series.models import Series
from videos.models import Listing


class SeriesCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    model = Series
    template_name = 'dashboard/series/createSeries.html'
    form_class = SeriesForm
    success_message = "%(title)s was created successfully"

    def form_valid(self, form):
        self.created_series = self.create_series(form)
        return super(SeriesCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SeriesCreate, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs['website_id']
        return context

    def create_series(self, form):
        """Set the creator_id of the newly created series to the user that's 
        currently logged in and also fills in the title and description fields
        """

        series = Series(title=form.cleaned_data['title'], description=form.cleaned_data['description'],
                        creator_id=self.request.user.id, site_id=self.kwargs['website_id'])
        series.save()
        return series

    def get_success_url(self):
        return reverse('series:view', kwargs={
            'website_id': self.kwargs.get('website_id'),
            'series_id': self.created_series.id
        })


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


class SeriesEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Series

    fields = ['title', 'description', 'thumbnail']
    template_name = 'dashboard/series/editSeries.html'
    success_message = "%(title)s was updated!"

    def get_context_data(self, **kwargs):
        context = super(SeriesEdit, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs.get('website_id')
        context['pk'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse('series:view', kwargs={
            'website_id': self.kwargs.get('website_id'),
            'series_id': self.kwargs.get('pk')
        })


class SeriesDelete(LoginRequiredMixin, DeleteView):
    model = Series

    template_name = 'dashboard/series/deleteSeries.html'
    success_message = '%(title)s has been deleted.'

    def get_context_data(self, **kwargs):
        context = super(SeriesDelete, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs.get('website_id')
        context['pk'] = self.kwargs.get('pk')
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SeriesDelete, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('websites_dashboard', kwargs={
            'website_id': self.kwargs.get('website_id')
        })
