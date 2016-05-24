from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import CreateView

from videos.forms import VideoForm
from videos.models import Video


class VideoCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Renders video upload form and defines form submission behavior.

    First, validates request by redirecting to login page if user isn't logged
    in or 403s if user isn't the site creator. Passes website_id to view, and
    adds creator_id and site_id to Video model after submission.
    """

    login_url = '/account/login/'

    model = Video
    form_class = VideoForm
    template_name = 'dashboard/videos/create.html'

    success_message = "%(title)s was created successfully."

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
        form.instance.site = Site.objects.get(pk=self.kwargs['website_id'])
        form.instance.creator = self.request.user
        return super(VideoCreate, self).form_valid(form)

    def get_success_url(self):
        """Redirects to videos list view for site given in named arguments.

        Need to use reverse_lazy instead of reverse because the URLs have not
        been loaded when this file is imported.
        """
        return reverse_lazy('videos:index', kwargs={'website_id': self.kwargs['website_id']})


class VideoIndexView(generic.ListView):
    """Renders videos list view.

    Passes video_list iterable to template, which is set up by get_queryset.
    Also passes website_id URL parameter for link to site's upload form.
    """

    template_name = 'dashboard/videos/index.html'
    context_object_name = 'video_list'

    def get_context_data(self, **kwargs):
        """Provides the website_id context to the videos:index view."""
        context = super(VideoIndexView, self).get_context_data(**kwargs)
        context['website_id'] = self.kwargs['website_id']
        return context

    def get_queryset(self):
        """Gets videos belonging to current site and logged in user."""
        site = Site.objects.get(pk=self.kwargs['website_id'])
        return Video.objects.filter(site=site)
