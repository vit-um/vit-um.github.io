from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="user_followers")
    following = models.ManyToManyField("User", related_name="user_following")
    
    def __str__(self):
        return f"{self.id}: {self.username} {self.email} {self.followers} {self.following}"

    
# class Posts(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
    