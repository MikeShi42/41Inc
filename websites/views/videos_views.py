from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from videos.models import Video


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
