# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 13:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20160520_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='movie_file',
            field=models.FileField(null=True, upload_to='movie/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='resource',
            name='post',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='blog.Post'),
            preserve_default=False,
        ),
    ]
