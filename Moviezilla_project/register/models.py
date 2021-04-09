from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=150)
    drama=models.BooleanField(default=False)
    thriller=models.BooleanField(default=False)
    action=models.BooleanField(default=False)
    comedy=models.BooleanField(default=False)
    romance=models.BooleanField(default=False)
    adventure=models.BooleanField(default=False)

