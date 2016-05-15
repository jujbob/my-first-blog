# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160515_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='filtered_image_file',
            field=models.ImageField(blank=True, upload_to='WebApps/media/image/filtered/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='image_file',
            field=models.ImageField(blank=True, upload_to='WebApps/media/image/original/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='movie_file',
            field=models.FileField(blank=True, upload_to='WebApps/media/movie/%Y/%m/%d'),
        ),
    ]