from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.db.models import Max

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

    success_message = "%(title)s was created successfully!"

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

        messages.success(self.request, self.success_message % video.title)

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


class VideoIndexView(ListView):
    """Renders videos list view.

    Passes video_list iterable to template, which is set up by get_queryset.
    Also passes website_id URL parameter for link to site's upload form.
    """

    template_name = 'websites/videos/index.html'
    context_object_name = 'video_list'

    def get_context_data(self, **kwargs):
        """Provides the website_id context to the videos:index view."""
        context = super(VideoIndexView, self).get_context_data(**kwargs)
        context['website_id'] = get_current_site(self.request).id
        return context

    def get_queryset(self):
        """Gets videos belonging to current site and logged in user."""
        site = get_current_site(self.request)
        return Video.objects.filter(site=site)


class VideoDetailView(DetailView, SingleObjectTemplateResponseMixin):
    model = Video
    template_name = 'websites/videos/detail.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        return context


def detail(request, video_id):
    video_info = _format_video_response(Video.objects.get(pk=video_id))
    site_videos = Video.objects.filter(site=get_current_site(request)).exclude(pk=video_id)

    playlist_videos = []
    for video in site_videos:
        info = _format_video_response(video)
        playlist_videos += [info]

    response = [video_info] + playlist_videos

    print(response)
    return JsonResponse(response, safe=False)


def _format_video_response(video):
    video_info = {'name': video.title,
                  'description': video.description,
                  'duration': 45,
                  'sources': [
                      {'src': video.url, 'type': 'video/mp4'}
                  ],
                  'thumbnail': [
                      {'srcset': video.thumbnail.url, 'type': 'image/jpeg'}
                  ],
                  }
    return video_info
