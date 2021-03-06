# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20160605_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='filtered_image_file',
            field=models.ImageField(null=True, upload_to='image/post/filtered/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='image_file',
            field=models.ImageField(upload_to='image/post/original/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='movie_file',
            field=models.FileField(null=True, upload_to='movie/post/%Y/%m/%d'),
        ),
    ]
