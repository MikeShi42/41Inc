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
    main_color = models.TextField()
    mainbg_color = models.TextField()
    nav_color = models.TextField()
    navbg_color = models

    # Logo
    logo = models.ImageField(upload_to='logos')

    # Pitch information
    
