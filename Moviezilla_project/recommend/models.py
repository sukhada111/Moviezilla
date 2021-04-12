from django.db import models

# Create your models here.
from django.contrib.auth.models import User


# Create your models here.
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie_name=models.TextField()