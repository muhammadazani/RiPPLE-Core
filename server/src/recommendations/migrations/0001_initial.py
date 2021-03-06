# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-19 05:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='AvailableRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudyRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(unique=True)),
                ('end', models.TimeField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='availablerole',
            name='study_role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.StudyRole'),
        ),
        migrations.AddField(
            model_name='availablerole',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Topic'),
        ),
        migrations.AddField(
            model_name='availability',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.Day'),
        ),
        migrations.AddField(
            model_name='availability',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.Time'),
        ),
    ]
