# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-11 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20170410_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
