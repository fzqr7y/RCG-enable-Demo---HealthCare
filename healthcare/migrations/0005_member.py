# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 15:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('healthcare', '0004_auto_20160903_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=12)),
                ('tax_id', models.CharField(max_length=12)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=1)),
                ('birth_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('address', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=20, null=True)),
                ('state', models.CharField(max_length=2, null=True)),
                ('zip', models.CharField(max_length=10, null=True)),
                ('office_phone', models.CharField(max_length=20, null=True)),
                ('mobile_phone', models.CharField(max_length=20, null=True)),
                ('email', models.CharField(max_length=40, null=True)),
                ('social', models.CharField(max_length=40, null=True)),
                ('medical_risk', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('pharmacy_risk', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('plan_name', models.CharField(max_length=40, null=True)),
                ('plan_start', models.DateTimeField(null=True)),
                ('plan_end', models.DateTimeField(null=True)),
                ('plan_deductible', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('plan_oop_max', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]