# from django.shortcuts import render, redirect
# from .forms import RegisterForm

# def register(response):
#     if response.method == "POST":
# 	    form = RegisterForm(response.POST)
# 	    if form.is_valid():
# 	      form.save()

# 	    return redirect("/home")
#     else:
# 	    form = RegisterForm()

#     return render(response, "register/register.html", {"form":form})

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
#if username already exists error
from django.db import IntegrityError
#for login
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


def signupuser(request):
    if request.method=='GET':
        return render(request,'register/register.html',{'form':UserCreationForm()})
    else:
        #create a new user
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request,'register/register.html',{'form':UserCreationForm(),'error':'This username is already taken. Please choose a different username'})
        else:
            return render(request,'register/register.html',{'form':UserCreationForm(),'error':'Passwords did not match'})
    

def loginuser(request):
    if request.method=='GET':
        return render(request,'registration/login.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'registration/login.html',{'form':AuthenticationForm(),'error':'Username and Password did not match'})
        else:
            login(request,user)
            return redirect('home')

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

