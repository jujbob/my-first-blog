# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 07:41
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_remove_account_small_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]