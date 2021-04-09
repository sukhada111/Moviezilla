# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import User


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(max_length=150)
#     drama=forms.BooleanField()
#     thriller=forms.BooleanField()
#     action=forms.BooleanField()
#     comedy=forms.BooleanField()
#     romance=forms.BooleanField()
#     adventure=forms.BooleanField()

#     class Meta:
# 	    model = User
# 	    fields = ("username", "email", "password1", "password2","drama","thriller","action","comedy","romance","adventure")
        

from django.forms import ModelForm
from .models import Genre

class GenreForm(ModelForm):
    class Meta:
        model=Genre
        fields=['email','drama','thriller','action','comedy','romance','adventure']