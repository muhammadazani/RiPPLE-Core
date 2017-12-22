# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-22 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
