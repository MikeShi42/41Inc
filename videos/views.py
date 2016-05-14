from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from videos.forms import VideoForm
from videos.models import Video


class VideoCreate(LoginRequiredMixin, CreateView):
    login_url = '/account/login/'

    model = Video
    form_class = VideoForm
    template_name = 'videos/create.html'

    def get_context_data(self, **kwargs):
        """
        Provides the site_id context variable to the videos:create view.
        """
        context = super(VideoCreate, self).get_context_data(**kwargs)
        context['site_id'] = self.kwargs['site_id']
        return context

    def form_valid(self, form):
        """
        Sets creator_id to the user that's currently logged in and gets the
        site ID from the named arguments in the URL. Afterwards, redirects to
        the success URL.
        """
        site = Site.objects.get(pk=self.kwargs['site_id'])
        form.instance.site = site
        form.instance.creator = self.request.user
        return super(VideoCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Redirects to videos list view for site given in named arguments. Need
        to use reverse_lazy instead of reverse because the URLs have not been
        loaded when this file is imported.
        """
        return reverse_lazy('videos:index', kwargs={'site_id': self.kwargs['site_id']})


class IndexView(generic.ListView):
    template_name = 'videos/index.html'
    context_object_name = 'video_list'

    def get_context_data(self, **kwargs):
        """
        Provides the site_id context to the videos:index view.
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        context['site_id'] = self.kwargs['site_id']
        return context

    def get_queryset(self):
        """
        Gets all videos that belong to both the current site and the currently
        logged in user.
        """
        site = Site.objects.get(pk=self.kwargs['site_id'])
        return Video.objects.filter(site=site)
