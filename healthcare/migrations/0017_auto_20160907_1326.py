# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 17:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0016_auto_20160907_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providermember',
            name='member',
        ),
        migrations.RemoveField(
            model_name='providermember',
            name='provider',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='members',
        ),
        migrations.DeleteModel(
            name='ProviderMember',
        ),
    ]