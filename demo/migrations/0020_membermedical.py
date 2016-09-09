# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 13:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0019_provider_picture_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberMedical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(max_length=40)),
                ('measure_type', models.CharField(max_length=40)),
                ('measure_label', models.CharField(max_length=40)),
                ('is_current', models.NullBooleanField()),
                ('value_str', models.CharField(max_length=40, null=True)),
                ('value_1', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('value_2', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('value_1_tgt_hi', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('value_2_tgt_lo', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('value_1_alert_hi', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('value_2_alert_lo', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('measure_date', models.DateField(auto_now_add=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Member')),
            ],
        ),
    ]