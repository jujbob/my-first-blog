# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-18 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20160618_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='small_image',
            field=models.ImageField(upload_to='image/profile/%Y/%m/%d'),
        ),
    ]
