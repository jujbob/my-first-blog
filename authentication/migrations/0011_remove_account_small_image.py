# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-05 08:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_userimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='small_image',
        ),
    ]
