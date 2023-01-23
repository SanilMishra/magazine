from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection


# Create your views here.

def home(request):
    return render(request,'index.html')

def login(request):
    if request.method == "POST":
        dict1 = request.POST
        print(dict1)
    return render(request,'login.html')

def view_magazine(request):
    return render(request,'magazine.html')