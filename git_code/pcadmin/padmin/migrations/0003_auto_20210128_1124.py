# Generated by Django 3.0.6 on 2021-01-28 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padmin', '0002_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(upload_to='img/%y'),
        ),
    ]
