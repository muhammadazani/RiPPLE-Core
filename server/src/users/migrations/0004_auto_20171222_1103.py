# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-22 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171222_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='id',
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
    ]
