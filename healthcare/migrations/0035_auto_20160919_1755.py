# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0034_countydata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countydata',
            name='county',
            field=models.CharField(max_length=30),
        ),
    ]