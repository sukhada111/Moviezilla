from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# class Profile(models.Model):
#     user=models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )
#     email=models.EmailField(max_length=150)
#     drama=models.BooleanField(default=False)
#     thriller=models.BooleanField(default=False)
#     action=models.BooleanField(default=False)
#     comedy=models.BooleanField(default=False)
#     romance=models.BooleanField(default=False)
#     adventure=models.BooleanField(default=False)

# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(username=instance)
#     instance.profile.save()