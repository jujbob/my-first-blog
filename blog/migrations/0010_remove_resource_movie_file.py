# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 07:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_resource_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='movie_file',
        ),
    ]
