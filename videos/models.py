from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from series.models import Series


class Video(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='videos', null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    series = models.ManyToManyField(Series, related_name='videos')
    ratings = models.ManyToManyField(User, through='Rating')

    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.FileField(upload_to='videos')
    thumbnail = models.ImageField(upload_to='thumbnails')

    @property
    def url(self):
        """
        Shorthand model property for a video url for convenience. Instead of
        accessing the video Azure Storage URL with video.content.url, we can
        use just video.url.
        """
        return self.content.url

    def __str__(self):
        return "%s: %s" % (self.title, self.description)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    rating = models.IntegerField()

    def __str__(self):
        return "%s by <User: %s> on <Video: %s>" % (str(self.rating), self.user.username, self.video.title)
