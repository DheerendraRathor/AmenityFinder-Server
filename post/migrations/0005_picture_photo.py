# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 11:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='photo',
            field=models.ImageField(default=datetime.datetime(2016, 1, 6, 11, 24, 45, 798565, tzinfo=utc), upload_to=''),
            preserve_default=False,
        ),
    ]