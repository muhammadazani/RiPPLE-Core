# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-12 01:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_consentform_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='consent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]