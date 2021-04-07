from django.shortcuts import render

# Create your views here.
def dashb(request):
    return render(request,'recommend/dashboard.html')