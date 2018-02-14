# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-14 01:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0004_auto_20171222_1509'),
        ('users', '0004_auto_20171222_1103'),
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
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_time', models.DateTimeField()),
                ('user_status', models.CharField(max_length=20)),
                ('suggested_user_status', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('score', models.FloatField()),
                ('course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_user', to='users.CourseUser')),
                ('suggested_course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_course_user', to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedTopicRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.Recommendation')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
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
            model_name='request',
            name='study_role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.StudyRole'),
        ),
        migrations.AddField(
            model_name='request',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Topic'),
        ),
        migrations.AddField(
            model_name='recommendedtopicrole',
            name='study_role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.StudyRole'),
        ),
        migrations.AddField(
            model_name='recommendedtopicrole',
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
