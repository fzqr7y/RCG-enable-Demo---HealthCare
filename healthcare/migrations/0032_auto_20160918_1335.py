# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0031_auto_20160913_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='County_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('fips', models.IntegerField()),
                ('state', models.CharField(max_length=2)),
                ('state_name', models.CharField(max_length=20)),
                ('county', models.CharField(max_length=20)),
                ('measure_key', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=40)),
                ('measure_name', models.CharField(max_length=40)),
                ('measure_desc', models.TextField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='CountyMetrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('measure_key', models.CharField(max_length=10)),
                ('measure_name', models.CharField(max_length=40)),
                ('measure_desc', models.TextField(max_length=40)),
                ('val_1_key', models.CharField(max_length=10)),
                ('val_1_name', models.CharField(max_length=40)),
                ('val_1_desc', models.TextField(max_length=40)),
                ('val_2_key', models.CharField(max_length=10)),
                ('val_2_name', models.CharField(max_length=40)),
                ('val_2_desc', models.TextField(max_length=40)),
                ('val_3_key', models.CharField(max_length=10)),
                ('val_3_name', models.CharField(max_length=40)),
                ('val_3_desc', models.TextField(max_length=40)),
                ('val_4_key', models.CharField(max_length=10)),
                ('val_4_name', models.CharField(max_length=40)),
                ('val_4_desc', models.TextField(max_length=40)),
                ('val_5_key', models.CharField(max_length=10)),
                ('val_5_name', models.CharField(max_length=40)),
                ('val_5_desc', models.TextField(max_length=40)),
                ('val_6_key', models.CharField(max_length=10)),
                ('val_6_name', models.CharField(max_length=40)),
                ('val_6_desc', models.TextField(max_length=40)),
                ('val_7_key', models.CharField(max_length=10)),
                ('val_7_name', models.CharField(max_length=40)),
                ('val_7_desc', models.TextField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='CountyMetricWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('widget_name', models.CharField(max_length=20)),
                ('category', models.CharField(blank=True, max_length=40, null=True)),
                ('measure_name', models.CharField(max_length=20)),
                ('display_order', models.IntegerField(blank=True, null=True)),
                ('val1_col', models.CharField(blank=True, max_length=20, null=True)),
                ('val2_col', models.CharField(blank=True, max_length=20, null=True)),
                ('val3_col', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='county',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='county',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
