# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 15:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0038_county_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CountyMetricWidget',
        ),
    ]
