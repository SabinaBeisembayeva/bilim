# Generated by Django 3.2 on 2021-11-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_specialty'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Photo'),
        ),
    ]