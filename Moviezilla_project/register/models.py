from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Create your models here.
# class Genre(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     email=models.EmailField(max_length=150)
#     drama=models.BooleanField(default=False,null=True)
#     thriller=models.BooleanField(default=False,null=True)
#     action=models.BooleanField(default=False,null=True)
#     comedy=models.BooleanField(default=False,null=True)
#     romance=models.BooleanField(default=False,null=True)
#     adventure=models.BooleanField(default=False,null=True)

