from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    # Якщо користувач не увійшов до системи, повернутись на сторінку входу:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        # Отримуємо доступ до ім’я користувача та пароля з даних
        username = request.POST["username"]
        password = request.POST["password"]

        # Перевіряємо, чи ім’я користувача та пароль правильні, повертаємо об’єкт User, якщо все правильно
        user = authenticate(request, username=username, password=password)

        # Якщо об’єкт user повернуто, увійти до системи та повернутись на головну сторінку:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # У іншому випадку, повернутись до сторінки входу з новим контекстом
        else:
            return render(request, "users/login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
                "message": "Logged Out"
            })