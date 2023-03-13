from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", blank = True, verbose_name="Слідкую", related_name="followers")
    
    def __str__(self):
        return f"{self.id}: {self.username} ({self.first_name} {self.last_name})"

class Posts(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Автор допису")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час допису")
    post = models.TextField(blank=False, verbose_name="Текст допису")
    likes = models.IntegerField(default=0, verbose_name="Кількість лайків")  
    users_like = models.ManyToManyField("User", blank = True, verbose_name="Сподобалось користувачам", related_name="like_posts")

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "timestamp": self.timestamp.strftime("%d.%m.%y %H:%M"),
            "post": self.post,
            "likes": self.likes,
            "users_like": self.users_like
        }
        
    def __str__(self):
        return f"{self.id}: {self.author}"
    
    class Meta:
        verbose_name = "Дописи"
        verbose_name_plural = "Дописи"