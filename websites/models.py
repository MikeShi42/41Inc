from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models


class Info(models.Model):
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    description = models.TextField()
    premium_enabled = models.BooleanField(
        default=False
    )
    price_month = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )
    price_year = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )
    stripe_public_key = models.CharField(
        null=True,
        max_length=32
    )
    stripe_secret_key = models.CharField(
        null=True,
        max_length=32
    )
    stripe_user_id = models.CharField(
        null=True,
        max_length=32
    )
