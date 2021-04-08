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
# from .forms import RegisterForm


def signupuser(request):
    if request.method=='GET':
        # form=RegisterForm()
        return render(request,'register/register.html',{'form':UserCreationForm()})
    else:
        # form=RegisterForm(request.POST)
        # if form.is_valid():
            # user=form.save()
            # user.refresh_from_db()

            #create a new user
        if request.POST['password1']==request.POST['password2']:
                try:
                    user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                    user.save()
                    
                    # user.Profile.email = form.cleaned_data.get('email')
                    # user.Profile.user = form.cleaned_data.get('username')
                    # user.Profile.drama=form.cleaned_data.get('drama')
                    # user.Profile.action=form.cleaned_data.get('action')
                    # user.Profile.thriller=form.cleaned_data.get('thriller')
                    # user.Profile.comedy=form.cleaned_data.get('comedy')
                    # user.Profile.romance=form.cleaned_data.get('romance')
                    # user.Profile.adventure=form.cleaned_data.get('adventure')
                    # user.save()

                    
                    # password = form.cleaned_data.get('password1')
                    # username=form.cleaned_data.get('username')
                    # user=authenticate(username=username,password=password)
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

