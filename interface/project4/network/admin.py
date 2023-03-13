from django.contrib import admin
from .models import User, Posts

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email")
    filter_horizontal = ("following",)
    
class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "timestamp", "post", "likes")
    filter_horizontal = ("users_like",)
    
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostsAdmin)