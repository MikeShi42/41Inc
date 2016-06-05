from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Max
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.edit import UpdateView

from videos.forms import VideoForm
from videos.models import Video, Listing


class VideoCreate(PermissionRequiredMixin,CreateView):
    """Renders video upload form and defines form submission behavior.

    First, validates request by redirecting to login page if user isn't logged
    in or 403s if user isn't the site creator. Passes website_id to view, and
    adds creator_id and site_id to Video model after submission.
    """

    login_url = '/account/login/'

    model = Video
    form_class = VideoForm
    template_name = 'dashboard/videos/create.html'

    def has_permission(self):
        """Renders view only if logged-in user is site creator, or 403s."""
        site = Site.objects.get(pk=self.kwargs['website_id'])
        return site.info.creator == self.request.user

    def handle_no_permission(self):
        """Redirects user to dashboard if the user isn't authorized,"""
        messages.error(self.request, "You can't upload videos for this site!")
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        """Provides the website_id context variable to the videos:create view."""
        context = super(VideoCreate, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs['website_id']
        return context

    def form_valid(self, form):
        """Handles foreign key constraints on form submission.

        Sets creator_id to the user that's currently logged in and gets the
        site ID from the named arguments in the URL. Afterwards, redirects to
        the success URL.
        """
        video = form.save(commit=False)
        video.site = Site.objects.get(pk=self.kwargs['website_id'])
        video.creator = self.request.user
        video.save()

        messages.success(self.request, "%s was successfully created!" % video.title)

        if form.cleaned_data['series']:
            max_order = Listing.objects.filter(series=form.cleaned_data['series']).aggregate(Max('order'))['order__max']
            listing_order = 1 if max_order is None else max_order + 1
            listing = Listing(series=form.cleaned_data['series'][0], video=video, order=listing_order)
            listing.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        """Redirects to videos list view for site given in named arguments.

        Need to use reverse_lazy instead of reverse because the URLs have not
        been loaded when this file is imported.
        """
        # site = Site.objects.get(pk=self.kwargs['website_id'])
        # uri = reverse_lazy('videos:index', urlconf='websites.urls')
        return reverse('websites_dashboard', kwargs={
            'website_id': self.kwargs.get('website_id')
        })


class VideoEdit(SuccessMessageMixin, UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    login_url = '/account/login/'

    model = Video
    form_class = VideoForm
    template_name = 'websites/videos/update.html'

    success_message = "%(title)s was updated successfully."

    def has_permission(self):
        """Renders view only if logged-in user is site creator, or 403s."""
        site = Site.objects.get(pk=self.kwargs['website_id'])
        return site.info.creator == self.request.user

    def handle_no_permission(self):
        """Redirects user to dashboard if the user isn't authorized,"""
        messages.error(self.request, "You can't edit videos for this site!")
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super(VideoEdit, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs['website_id']
        return context

    def form_valid(self, form):
        video = form.save(commit=False)
        video.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('websites_dashboard', kwargs={
            'website_id': self.kwargs.get('website_id')
        })


class VideoDelete(LoginRequiredMixin, DeleteView):
    model = Video
    success_url = reverse_lazy('dashboard')
    template_name = 'dashboard/videos/delete.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDelete, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs.get('website_id')
        context['pk'] = self.kwargs.get('pk')
        return context

