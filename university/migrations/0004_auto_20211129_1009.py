# Generated by Django 3.2 on 2021-11-29 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0003_university_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='university',
        ),
        migrations.AddField(
            model_name='faculty',
            name='university',
            field=models.ManyToManyField(related_name='university_faculties', to='university.University', verbose_name='University'),
        ),
    ]
