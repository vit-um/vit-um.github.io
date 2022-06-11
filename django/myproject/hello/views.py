from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.

# def index(request): 
#     return HttpResponse("Hello, world!")

def index(request):
    now = datetime.datetime.now()
    return render(request, "hello/index.html", {
        "newyear": now.month == 6 and now.day == 11
    })


def brian(request):
    return HttpResponse("<h1 style=\"color:blue\">Hello, Brian!</h1>")

# def greet(request, name):
#     return HttpResponse(f"Hello, {name.capitalize()}!")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })


