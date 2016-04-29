from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Profile model that stores the additional attributes for the user such as the company.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="user")
    company = models.CharField(max_length=255, blank=True)


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
