from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

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
        video = form.save(commit=False)
        video.site = Site.objects.get(pk=self.kwargs['website_id'])
        video.creator = self.request.user
        video.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Redirects to videos list view for site given in named arguments.

        Need to use reverse_lazy instead of reverse because the URLs have not
        been loaded when this file is imported.
        """
        site = Site.objects.get(pk=self.kwargs['website_id'])
        uri = reverse_lazy('videos:index', urlconf='websites.urls')
        return 'http://%s%s' % (site.domain, uri)


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
        site = Site.objects.get(pk=self.kwargs['website_id'])
        uri = reverse_lazy('videos:index', urlconf='websites.urls')
        return 'http://%s%s' % (site.domain, uri)


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


def detail(video_id):
    video = Video.objects.get(pk=video_id)
    response = {'name': video.title,
                'description': video.description,
                'url': video.url,
                'sources': [
                    {'src': video.url, 'type': 'video/mp4'}
                ],
                'thumbnail': [
                    {'srcset': video.thumbnail.url, 'type': 'image/jpeg'}
                ],
                }
    # playlist_videos = list(Video.objects.all().exclude(pk=video_id))
    return JsonResponse(response, safe=False)
