from django.shortcuts import render
import requests

# Create your views here.
def homepage(request):
   
    return render(request,'index.html')
def aboutUs(request):
    return render(request,'aboutUs.html')
