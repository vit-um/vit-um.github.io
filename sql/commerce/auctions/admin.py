from django.contrib import admin
from .models import User, Category, Lots

class LotsAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "name", "description", "bid", "urlimage", "image", "status")

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Lots, LotsAdmin)
