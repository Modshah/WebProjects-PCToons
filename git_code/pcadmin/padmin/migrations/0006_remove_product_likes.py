# Generated by Django 3.0.6 on 2021-03-01 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('padmin', '0005_auto_20210227_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='likes',
        ),
    ]
