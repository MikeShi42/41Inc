from django import forms
from videos.models import Video


class VideoForm(forms.ModelForm):
    video_file = forms.FileField()

    class Meta:
        model = Video
        fields = ['title', 'description']
