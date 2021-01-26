from django.db import models



class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)
    image_path = models.CharField(max_length=500)
    tags = models.CharField(max_length=500)


class User(models.Model):
    pass


