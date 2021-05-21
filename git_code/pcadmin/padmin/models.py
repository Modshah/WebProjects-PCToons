from datetime import time

import requests
from django import forms
from django.contrib.auth.models import AbstractUser
from PIL import Image, ImageDraw, ImageFont
from django.utils.safestring import mark_safe

from .tag_selection import tags_choice
from django.contrib.auth.models import User
import os
from datetime import datetime
import sys
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_init
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField
import stripe

from django.conf import settings


class Image_Upload(models.Model):
    image_name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    # like = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='img/')
    # choice = forms.MultipleChoiceField(choices=tuple(tags_choice()))
    tags = models.CharField(max_length=1000)
    caption = models.CharField(max_length=200)
    countries = models.CharField(max_length=1000)

    # country = CountryField()
    # Author= models.CharField(max_length=200)

    # readonly_fields = [..., "image preview"]


@receiver(post_save, sender=Image_Upload)
def watermark(sender, instance, **kwargs):
    BASE = "http://127.0.0.1:5000/"
    PATH = "C:/Users/might/Desktop/Flask-Rest-API-Tutorial/WebProjects-PCToons/git_code/pcadmin/media/"
    print(instance.img)

    os.chdir(PATH)
    ##response = requests.put(BASE + "video/4", {"name": "gaurav", "views": "10", "id": "4", "likes": "10"})
    # response = requests.get(BASE + "users")
    file = str(instance.img)
    # (response.json())[6]
    im = Image.open(PATH + file)
    width, height = im.size
    im1 = Image.open(PATH + file)
    width2, height2 = im.size
    ##assert isinstance(im.size, object)

    compresssize = (int(width2 / 10), int(height2 / 10))
    im1 = im1.resize(compresssize)
    im1.save(PATH + file.replace('img', 'thumbnail'))

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

    im.save(PATH + file.replace('img', 'watermark'))
    if not (Image_Watermark.objects.filter(pk=instance.id).exists()):
        Image_Watermark.objects.create(
            id=instance.id,
            image_name=instance.image_name,
            image=instance.image,
            compress_img=file.replace('img', 'thumbnail'),
            watermarked_img=file.replace('img', 'watermark'),
            tags=instance.tags,
            caption=instance.caption,
            countries=instance.caption
        )

    else:
        Image_Watermark.objects.filter(pk=instance.id).update(
            image_name=instance.image_name,
            image=instance.image,
            compress_img='http://127.0.0.1:8000/' + file.replace('img', 'media/thumbnail'),
            watermarked_img='http://127.0.0.1:8000/'+file.replace('img', 'media/watermark'),
            tags=instance.tags,
            caption=instance.caption,
            countries=instance.caption
        )

    if not (tags.objects.filter(image_id=instance.id).exists()):

        tag_var = str(instance.tags)
        #assert isinstance(tag_var.split, object)
        for i in tag_var.split():
            tags.objects.create(
                tag_Value=i,
                image_id=instance.id

            )
    else:
        tags.objects.filter(image_id=instance.id).delete()
        tag_var = str(instance.tags)
        # assert isinstance(tag_var.split, object)
        for i in tag_var.split():
            tags.objects.create(
                tag_Value=i,
                image_id=instance.id

            )
    if not (img_country.objects.filter(image_id=instance.id).exists()):

        tag_var = str(instance.countries)
        #assert isinstance(tag_var.split, object)
        for i in tag_var.split():
            img_country.objects.create(

                Country=i,
                image_id=instance.id

            )
    else:
        img_country.objects.filter(image_id=instance.id).delete()
        tag_var = str(instance.countries)
        # assert isinstance(tag_var.split, object)
        for i in tag_var.split():
            img_country.objects.create(

                Country=i,
                image_id=instance.id

            )


class Image_Watermark(models.Model):
    image_name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    # like = models.PositiveIntegerField(default=0)
    compress_img = models.CharField(max_length=200)
    watermarked_img = models.CharField(max_length=200)
    # choice = forms.MultipleChoiceField(choices=tuple(tags_choice()))
    tags = models.CharField(max_length=1000)
    caption = models.CharField(max_length=200)
    countries = models.CharField(max_length=1000)


class tags(models.Model):
    image_id = models.IntegerField()
    tag_Value = models.CharField(max_length=100)


##for exclusion of country
class img_country(models.Model):
    image_id = models.IntegerField()
    Country = models.CharField(max_length=100)

class license(models.Model):
    licenses = models.CharField(max_length=1000)
    licenses_desc = models.CharField(max_length=16383)
    cost = models.IntegerField()


class subscribers(models.Model):
    subscriber_email = models.CharField(max_length=200)
    subscriber_name = models.CharField(max_length=200)
    active_flag = models.CharField(max_length=200)


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class User(models.Model):
    pass
