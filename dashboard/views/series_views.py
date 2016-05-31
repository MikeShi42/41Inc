from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, UpdateView
from series.forms import SeriesForm
from django.core.exceptions import ValidationError
from django.views.generic.list import ListView
from django.contrib.sites.models import Site
from series.models import Series
from videos.models import Listing
from django.core.urlresolvers import reverse

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

