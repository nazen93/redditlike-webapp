# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-02 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('r', '0050_remove_posttext_voted'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttext',
            name='is_promoted',
            field=models.BooleanField(default=False),
        ),
    ]
