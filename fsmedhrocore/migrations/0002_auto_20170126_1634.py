# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsmedhrocore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gender',
            name='endung',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]