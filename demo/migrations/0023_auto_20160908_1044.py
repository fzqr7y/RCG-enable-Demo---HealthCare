# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0022_auto_20160908_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='membermedical',
            name='value_1_trend',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True),
        ),
        migrations.AddField(
            model_name='membermedical',
            name='value_2_trend',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True),
        ),
    ]
