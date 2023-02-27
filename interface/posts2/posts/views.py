import time

from django.http import JsonResponse
from django.shortcuts import render

# Створіть ваші представлення
def index(request):
    return render(request, "posts/index.html")

def posts(request):

    # Отримати точки початку та кінця
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    # Згенерувати список дописів
    data = []
    for i in range(start, end + 1):
        data.append(f"Допис №{i} нашого форуму")

    # Спеціально уповільнити швидкість відповіді
    time.sleep(1)

    # Повернути список дописів
    return JsonResponse({
        "posts": data
    })
