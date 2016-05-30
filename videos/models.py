from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from series.models import Series
from validators import validate_video_file


class Video(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='videos', null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    series = models.ManyToManyField(Series, through='Listing')
    ratings = models.ManyToManyField(User, through='Rating')

    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.FileField(upload_to='videos', validators=[validate_video_file])
    thumbnail = models.ImageField(upload_to='thumbnails')

    views = models.PositiveIntegerField(default=0)

    @property
    def url(self):
        """Shorthand model property for a video url for convenience.

        Instead of accessing the video Azure Storage URL with video.content.url,
        we can use just video.url.
        """
        return self.content.url

    @property
    def rating(self):
        return sum([x.rating for x in self.ratings.all()])

    def __str__(self):
        return "%s - %s" % (self.title, self.description)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    rating = models.IntegerField()

    def __str__(self):
        return "%s by %s on %s" % (str(self.rating), self.user, self.video)


class Listing(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='listings')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='listings')

    order = models.IntegerField()

    def __str__(self):
        return "%s - #%d in %s" % (self.video, int(self.order), self.series)

    class Meta:
        unique_together = (('series', 'order'), ('series', 'video'))
        ordering = ['order']
