from django import forms
from videos.models import Video


class VideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['series'].required = False

    class Meta:
        model = Video
        fields = ['series', 'title', 'description', 'content', 'thumbnail']
        labels = {
            'content': 'Video'
        }
        help_texts = {
            'series': "Choose which series to put this new video in, or leave blank if the video doesn't belong to a "
                      "series.",
            'content': 'Choose the video file to upload.',
            'thumbnail': "Choose an image that will appear as the video's thumbnail."
        }
