# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-21 23:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_auto_20170121_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='privatemessage',
            old_name='message',
            new_name='body',
        ),
    ]
