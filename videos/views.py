from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView

from videos.models import Video


class VideoCreate(LoginRequiredMixin, CreateView):
    login_url = '/account/login'

    model = Video
    fields = ['title', 'description', 'url', 'thumbnail_url']
    template_name = 'videos/create.html'

    def form_valid(self, form):
        video = form.save(commit=False)
        video.user = User.objects.get(user=self.request.user)
        video.save()


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/account/login'

    template_name = 'videos/index.html'
    context_object_name = 'video_list'

    def get_queryset(self):
        return Video.objects.filter(creator=self.request.user)
