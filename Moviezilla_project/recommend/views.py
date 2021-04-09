
from django.shortcuts import render,redirect,get_object_or_404

from register.models import Genre
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashb(request):
    genres=get_object_or_404(Genre,user=request.user)
    return render(request,'recommend/dashboard.html',{'gen':genres})