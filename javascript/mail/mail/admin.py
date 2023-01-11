from django.contrib import admin
from .models import User, Email

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "date_joined")

class MailAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body", "read", "archived","sender_id", "user_id")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Email, MailAdmin)
