# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('r', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlink',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AddField(
            model_name='posttext',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
