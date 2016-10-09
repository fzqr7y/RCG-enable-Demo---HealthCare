# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0039_delete_countymetricwidget'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountyWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('widget_name', models.CharField(max_length=20)),
                ('category', models.CharField(blank=True, max_length=40, null=True)),
                ('measure_name', models.CharField(max_length=20)),
                ('display_order', models.IntegerField(blank=True, null=True)),
                ('val1_ref', models.CharField(blank=True, max_length=20, null=True)),
                ('val2_ref', models.CharField(blank=True, max_length=20, null=True)),
                ('val3_ref', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]