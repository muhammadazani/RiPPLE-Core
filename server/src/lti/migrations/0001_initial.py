# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-19 05:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LTIConfiguration',
            fields=[
                ('consumer_key', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('secret_key', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.PositiveIntegerField()),
                ('nonce', models.CharField(max_length=255)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lti.LTIConfiguration')),
            ],
        ),
    ]
