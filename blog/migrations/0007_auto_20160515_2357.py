# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160515_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='image_file',
            field=models.ImageField(upload_to='image/original/%Y/%m/%d'),
        ),
    ]
