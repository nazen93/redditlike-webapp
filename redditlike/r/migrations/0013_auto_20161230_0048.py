# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-29 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('r', '0012_voter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttext',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='/static/'),
        ),
    ]
