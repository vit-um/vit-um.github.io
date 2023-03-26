import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts


def index(request):
    posts = Posts.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        "posts": posts
    })

def following(request):
    users =  request.user.followers.all() # User.objects.filter(username = request.user)
    # us_id = []
    # for user in users:
    #     us_id = user.id
#    auth = user.all() #.followers.all()
    posts = Posts.objects.filter(author = users.first().id).order_by('-timestamp')
    return render(request, "network/index.html", {
        "auth": users,
        "posts": posts
    })


def filter(request, filter):
    users =  request.user.followers.all()
    if filter == "all":
        posts = Posts.objects.all().order_by('-timestamp')
    elif filter == "following":
        posts = Posts.objects.filter(author = users.first().id).order_by('-timestamp')
    else: 
        return render(request, "network/index.html", "ERROR")
    
    return JsonResponse([post.serialize() for post in posts], safe=False)

    # return render(request, "network/index.html", {
    #     "auth": users,
    #     "posts": posts
    # })
    
def post(request, post_id):
    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def admin(request):
    return render(request, "admin/")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        
        # Ensure username or email is not empty
        if len(username) < 2 or len(email) < 3:
            return render(request, "network/register.html", {
                "message": "Хибний логін або електрона адреса"
            })
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Паролі повинні збігатися"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
