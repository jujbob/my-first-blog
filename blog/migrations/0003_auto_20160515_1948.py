# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='filtered_image_file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='resource',
            name='image_file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='resource',
            name='movie_file',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
