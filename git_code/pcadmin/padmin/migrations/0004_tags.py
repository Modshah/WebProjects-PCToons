# Generated by Django 3.0.6 on 2021-02-06 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padmin', '0003_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_Value', models.CharField(max_length=50)),
            ],
        ),
    ]
