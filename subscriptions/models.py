"""Defines models used related to subscription handling"""
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models

"""Keeps records of customers who have active subscriptions"""
class Subscription(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    customer_id = models.CharField(
        verbose_name='Customer ID',
        max_length=64
    )
    active_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

"""Keeps track of admin settings for subscription prices"""
class Settings(models.Model):
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        primary_key=True
    )
    premium_enabled = models.BooleanField(
        verbose_name='Premium Enabled',
        help_text='Videos that are marked premium will force users to subscribe before being able to view them.',
        default=False
    )
    price_month = models.DecimalField(
        verbose_name='Monthly Price',
        help_text='Users will charged this amount per month for premium access.',
        max_digits=6,
        decimal_places=2,
        default=0.00
    )
    price_year = models.DecimalField(
        verbose_name='Annual Price',
        help_text='Users will charged this amount per month for premium access.',
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
