from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.page, name="page"),
    path("edit/", views.edit, name="edit"),
    path("new/", views.new, name="new"),
    path("save/", views.save, name="save"),
    path("random", views.random_page, name="random_page"),
    path("search/", views.search, name="search")
]
