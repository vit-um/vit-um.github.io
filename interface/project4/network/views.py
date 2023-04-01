import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Posts


def index(request):
    posts = Posts.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        "posts": posts
    })

def filter(request, filter):
    if filter == "all":
        posts = Posts.objects.all().order_by('-timestamp')
    elif filter == "following":
        users =  request.user.followers.all()
        posts = Posts.objects.filter(author = users.first().id).order_by('-timestamp')
    else: 
        return render(request, "network/index.html", "ERROR")
    
    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    # Update whether post is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liker") == 1:
            tmp = post.likes + 1
            post.likes = tmp
            post.users_like.add(request.user)
        else:
            tmp = post.likes - 1
            post.likes = tmp  
            post.users_like.remove(request.user)                   
        post.save()
        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def compose(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    post = Posts(
        author=request.user,
        post=data.get("body", "")
    )
    post.save()
    return JsonResponse({"message": "Ваш пост успішно розміщено у мережі."}, status=201)


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
    
