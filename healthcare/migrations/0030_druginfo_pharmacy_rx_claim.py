# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 22:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0029_auto_20160912_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('drug_ndc', models.CharField(max_length=12)),
                ('drug_name', models.CharField(max_length=20)),
                ('drug_details', models.CharField(max_length=40)),
                ('drug_type', models.CharField(max_length=20)),
                ('therapeutic_class', models.CharField(max_length=20)),
                ('pkg_quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pkg_units', models.CharField(max_length=10)),
                ('days_supply', models.DecimalField(decimal_places=0, max_digits=4)),
                ('dose', models.DecimalField(decimal_places=4, max_digits=10)),
                ('dose_units', models.CharField(max_length=10)),
                ('take_quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('take_units', models.CharField(max_length=10)),
                ('take_frequency', models.DecimalField(decimal_places=0, max_digits=2)),
                ('frequency_units', models.CharField(max_length=10)),
                ('take_instructions', models.CharField(max_length=40)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('pharmacy_key', models.CharField(max_length=20)),
                ('pharmacy_name', models.CharField(max_length=20)),
                ('pharmacy_chain', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Rx_Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('drug_ndc', models.CharField(max_length=12)),
                ('drug_name', models.CharField(max_length=20)),
                ('drug_details', models.CharField(max_length=40)),
                ('drug_type', models.CharField(max_length=20)),
                ('therapeutic_class', models.CharField(max_length=20)),
                ('pharmacy_key', models.CharField(max_length=20)),
                ('pharmacy_name', models.CharField(max_length=20)),
                ('pharmacy_chain', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=40)),
                ('prescription_ref', models.CharField(max_length=20)),
                ('prescribed_date', models.DateTimeField()),
                ('filled_date', models.DateTimeField()),
                ('refills_prescribed', models.DecimalField(decimal_places=0, max_digits=2)),
                ('refills_remaining', models.DecimalField(decimal_places=0, max_digits=2)),
                ('script_quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('script_units', models.CharField(max_length=10)),
                ('days_supply', models.DecimalField(decimal_places=0, max_digits=4)),
                ('dose', models.DecimalField(decimal_places=4, max_digits=10)),
                ('dose_units', models.CharField(max_length=10)),
                ('take_quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('take_units', models.CharField(max_length=10)),
                ('take_frequency', models.DecimalField(decimal_places=0, max_digits=2)),
                ('frequency_units', models.CharField(max_length=10)),
                ('take_instructions', models.CharField(max_length=40)),
                ('billed', models.DecimalField(decimal_places=2, max_digits=8)),
                ('allowed', models.DecimalField(decimal_places=2, max_digits=8)),
                ('plan_paid', models.DecimalField(decimal_places=2, max_digits=8)),
                ('member_paid', models.DecimalField(decimal_places=2, max_digits=8)),
                ('plan_deductible', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_current', models.NullBooleanField()),
                ('druginfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthcare.DrugInfo')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthcare.Member')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthcare.Pharmacy')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthcare.Provider')),
            ],
        ),
    ]
