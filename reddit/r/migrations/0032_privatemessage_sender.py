# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 01:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('r', '0031_privatemessage_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatemessage',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
