# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-15 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('r', '0025_remove_posttext_has_voted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posttext',
            name='vote_status',
        ),
    ]
