from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic
from django.views.generic.edit import CreateView

from videos.models import Video
from videos.forms import VideoForm


class VideoCreate(LoginRequiredMixin, CreateView):
    login_url = '/account/login'
    success_url = '/videos'

    model = Video
    form_class = VideoForm
    template_name = 'videos/create.html'

    def form_valid(self, form):
        """
        Sets creator_id to the user that's currently logged in.
        """
        form.instance.creator = self.request.user
        return super(VideoCreate, self).form_valid(form)


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/account/login'

    template_name = 'videos/index.html'
    context_object_name = 'video_list'

    def get_queryset(self):
        return Video.objects.filter(creator=self.request.user)
