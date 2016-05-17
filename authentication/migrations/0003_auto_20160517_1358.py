# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 04:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20160415_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and ./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.+-]+$', 'Enter a valid username jebal.', 'invalid')], verbose_name='username'),
        ),
    ]
