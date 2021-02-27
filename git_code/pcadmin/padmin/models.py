from datetime import time

import requests
from django import forms
from django.contrib.auth.models import AbstractUser
from PIL import Image, ImageDraw, ImageFont
from .tag_selection import tags_choice
from django.contrib.auth.models import User
import os
from datetime import datetime
import sys
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_init
from multiselectfield import MultiSelectField


class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)
    image_path = models.CharField(max_length=500)
    img = models.ImageField(upload_to='img/')
    #choice = forms.MultipleChoiceField(choices=tuple(tags_choice()))
    tags = models.CharField(max_length=500)
    caption = models.CharField(max_length=200)


@receiver(post_init, sender=Product)
def watermark(sender, instance, **kwargs):

    BASE = "http://127.0.0.1:5000/"
    PATH = "C:/Users/guddu/Desktop/Flask-Rest-API-Tutorial/WebProjects-PCToons/git_code/pcadmin/media/"

    os.chdir(PATH)
    ##response = requests.put(BASE + "video/4", {"name": "gaurav", "views": "10", "id": "4", "likes": "10"})
    response = requests.get(BASE + "users")
    file = (response.json())[6]
    im = Image.open(PATH + file)
    width, height = im.size

    newsize = (int(width / 5), int(height / 5))
    im = im.resize(newsize)
    width, height = im.size
    draw = ImageDraw.Draw(im)
    text = "pareshcartoon"

    font = ImageFont.truetype('arial.ttf', 36)
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin

    # draw watermark in the bottom right corner

    draw.text((1, 1), text, font=font)
    draw.text((x, y), text, font=font)
    draw.text((x / 2, y / 2), text, font=font)
    draw.text((1, y), text, font=font)
    draw.text((x, 1), text, font=font)
    draw.text((1, y / 2), text, font=font)
    draw.text((x / 2, 1), text, font=font)
    draw.text((1, y / 4), text, font=font)
    draw.text((x / 4, y), text, font=font)
    draw.text((x, y / 4), text, font=font)
    draw.text((7 * x / 8, 7 * y / 8), text, font=font)
    draw.text((1, 7 * y / 8), text, font=font)
    draw.text((x / 2, 7 * y / 8), text, font=font)
    draw.text((7 * x / 8, y), text, font=font)

    # Save watermarked image

    im.save(PATH+file.replace('img', 'watermark'))


class User(models.Model):
    pass
