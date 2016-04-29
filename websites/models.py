from __future__ import unicode_literals

from django.db import models


class Website(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    domain = models.CharField(max_length=255)
