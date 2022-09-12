from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("active", views.active, name="active"),
    path("mylots", views.mylots, name="mylots"),
    path("newlot", views.newlot, name="newlot"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("cat/<str:cat>", views.catview, name="catview"),
    path("lot<int:lotID>", views.lotpage, name="lotpage"),
    path("search", views.search, name="search")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
