# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-23 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rippleAchievements', '0007_task_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='achievements',
            field=models.ManyToManyField(to='rippleAchievements.Achievement'),
        ),
        migrations.AddField(
            model_name='task',
            name='views',
            field=models.ManyToManyField(to='rippleAchievements.View'),
        ),
    ]
