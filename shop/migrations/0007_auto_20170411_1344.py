# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_about'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='url_photo',
        ),
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='products/none.jpg', upload_to='products'),
        ),
    ]
