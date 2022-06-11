from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

# tasks = ["foo", "bar", "baz"] 

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1,max_value=10)

# Create your views here.
# def index(request):
#     return render(request, "tasks/index.html", {
#         "tasks": tasks
#     })

def index(request):
    # Перевіряємо, чи ключ «завдання» вже існує у нашій сесії
    if "tasks" not in request.session:
        # Якщо ні, створюємо новий список
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })



# def add(request):
#     return render(request, "tasks/add.html")

def add(request):
    # Перевіряємо, чи метод є методом POST
    if request.method == "POST":
        # Отримуємо дані, відправлені користувачем, і зберігаємо їх у вигляді форми
        form = NewTaskForm(request.POST)
        # Перевіряємо, чи дані форми дійсні (зі сторони сервера) 
        if form.is_valid():
            # Відділяємо завдання від «очищеної» версії даних форми 
            task = form.cleaned_data["task"]
            # Додаємо нове завдання до нашого списку завдань 
            # tasks.append(task)
            request.session["tasks"] += [task]
            # Перенаправлюємо користувача до списку завдань
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            # Якщо форма недійсна, повторно візуалізуємо сторінку з наявною інформацією.
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
    