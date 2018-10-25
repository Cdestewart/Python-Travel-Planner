# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-17 17:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='first_app.User'),
            preserve_default=False,
        ),
    ]
