from django.forms import ModelForm
from videos.models import Video


class VideoForm(ModelForm):
    class Meta:
        model = Video
