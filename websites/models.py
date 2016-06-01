from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models


class Info(models.Model):
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    # Customization fields
    main_color = models.TextField(default="#fff")
    main_bg_color = models.TextField(default="#666")

    # Logo
    logo = models.ImageField(null=True, upload_to='logos')

    # Pitch information
    header = models.TextField(default="Start Learning Now")
    sub_header = models.TextField(default="We're the go-to source of tutorials on the web")

    # Reasons to subscribe
    subscribe_pitch = models.TextField(default="Be part of a revolution")
