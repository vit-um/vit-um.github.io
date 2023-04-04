from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", blank = True, verbose_name="Слідкую", related_name="followers")
    
    def serialize(self):
        return {
            "username": self.username, 
            "last_login": self.last_login.strftime("%d.%m.%y %H:%M"),
            "email": self.email,
            "following": list(self.following.values_list('username', flat=True)),
        }
    
    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

class Posts(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Автор допису")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час допису")
    post = models.TextField(blank=False, verbose_name="Текст допису")
    likes = models.IntegerField(default=0, verbose_name="Кількість лайків")  
    users_like = models.ManyToManyField("User", blank = True, verbose_name="Сподобалось користувачам", related_name="like_posts")

    def serialize(self):
        return {
            "id": self.id,
            "author": [self.author.username, self.author.first_name, self.author.last_name ], 
            "timestamp": self.timestamp.strftime("%d.%m.%y %H:%M"),
            "post": self.post,
            "likes": self.likes,
            "users_like": list(self.users_like.values_list('username', flat=True)),
        }
        
    def __str__(self):
        return f"{self.id}: {self.author}"
    
    class Meta:
        verbose_name = "Дописи"
        verbose_name_plural = "Дописи"