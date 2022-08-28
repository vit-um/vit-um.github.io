from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import AppConfig



class User(AbstractUser):
    default_auto_field = 'django.db.models.AutoField'


class Category(models.Model):
    name = models.CharField(max_length = 64, blank = True)

    def __str__(self):
        return f"{self.id}: {self.name}"

class Lots(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "authorUser")
    name = models.CharField(max_length = 128)
    description = models.CharField(max_length = 2048)
    bid = models.DecimalField(max_digits = 7, decimal_places = 2)
    urlimage = models.URLField(max_length = 512, blank = True)
    image = models.ImageField(upload_to ="uploads/", blank = True, default="uploads/default.jpg")    
    category = models.ManyToManyField(Category, blank = True)
    wishlist = models.ManyToManyField(User, blank = True, related_name = "wishUsers")
    status = models.BooleanField(default = True)
    sold = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.id}: {self.name} by {self.author}"

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.CharField(max_length = 500, blank = False)
    lot = models.ForeignKey(Lots, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.id}: {self.author} {self.comment} {self.lot}"


class Bids(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    lot = models.ForeignKey(Lots, on_delete = models.CASCADE)
    userBid = models.DecimalField(max_digits = 7, decimal_places = 2)

    def __str__(self):
        return f"{self.id}: {self.lot} {self.author} {self.userBid}"        
            