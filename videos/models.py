from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from series.models import Series


class Video(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')

    ratings = models.ManyToManyField(User, through='Rating', related_name='ratings')

    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s" % (self.title, self.description)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    rating = models.IntegerField()

    def __str__(self):
        return "%s"
