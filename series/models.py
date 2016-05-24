from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db import models


class Series(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='series')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='series')

    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.CharField(max_length=255)

    def __str__(self):
        return "%s - %s" % (self.title, self.description)

