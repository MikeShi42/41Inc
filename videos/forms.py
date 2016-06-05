from django import forms

from series.models import Series
from videos.models import Video


class VideoForm(forms.ModelForm):
    """
    Form class for uploading videos to Azure Storage.
    """

    def __init__(self, *args, **kwargs):
        """
        Makes the series multiple-choice field on form not required, since some
        videos are independent videos who don't need no series.

        Some logic to get the form to load the correct sites
        """
        self.site = kwargs.pop('site')
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['series'].required = False

        # Filter series for current site
        self.fields['series'].queryset = Series.objects.filter(site=self.site)


    class Meta:
        model = Video
        fields = ['series', 'title', 'description', 'content', 'thumbnail', 'premium']
        labels = {
            'content': 'Video'
        }
        help_texts = {
            'series': "Choose which series to put this new video in, or leave blank if the video doesn't belong to a "
                      "series.",
            'content': 'Choose the video file to upload.',
            'thumbnail': "Choose an image that will appear as the video's thumbnail.",
            'premium': "Content marked premium will only be accessible to subscribers."
        }
