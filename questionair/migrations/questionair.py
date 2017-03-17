# -*- coding: utf-8 -*-
# Generated

from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('fsmedhrocore', 'questionair'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user',
                 models.OneToOneField(one_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),

        migrations.CreateModel(
            name='Fach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('Studienabschnitt', models.ManyToManyField(to='fsmedhrocore.Studienabschnitt')),
                ('Studiengang', models.ManyToManyField(to='fsmedhrocore.Studiengang')),
            ],
            options={
                'verbose_name': 'Fach',
                'verbose_name_plural': 'Fächer',
            },
        ),

        migrations.CreateModel(
            name='Klausur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('Fach', models.ManyToManyField(to='')),
                ('date', models.DateTimeField(default=datetime.datetime.today)),
            ],
            options={
                'verbose_name': 'Klausur',
                'verbose_name_plural': 'Klausuren',
            },
        ),

        migrations.CreateModel(
            name='Frage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('question', models.TextField()),
                ('answerA', models.TextField()),
                ('answerB', models.TextField()),
                ('answerC', models.TextField()),
                ('answerD', models.TextField()),
                ('answerE', models.TextField()),

                ('option1', models.TextField()),
                ('option2', models.TextField()),
                ('option3', models.TextField()),
                ('option4', models.TextField()),
                ('option5', models.TextField()),

                ('solution', models.CharField()),
            ],
        ),

        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commiter', models.ManyToManyField(to='fsmedhrocore.User')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('Frage', models.ManyToManyField(to='')),
                ('Text', models.TextField()),
            ],
        )
    ]