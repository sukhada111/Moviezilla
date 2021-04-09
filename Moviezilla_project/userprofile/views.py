from django.shortcuts import render,redirect,get_object_or_404

from register.models import Genre
from django.contrib.auth.decorators import login_required

@login_required
def userprofile(request):
    genres=get_object_or_404(Genre,user=request.user)
    return render(request,'userprofile/profile.html',{'gen':genres})

# Create your views here.
