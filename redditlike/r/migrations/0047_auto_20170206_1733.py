# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-06 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('r', '0046_auto_20170204_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttext',
            name='down_votes',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='posttext',
            name='up_votes',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
