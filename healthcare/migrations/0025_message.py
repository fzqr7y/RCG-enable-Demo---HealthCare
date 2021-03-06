# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-09 14:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('healthcare', '0024_auto_20160908_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(max_length=20)),
                ('message_from', models.CharField(max_length=20)),
                ('message_to', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('query_url', models.TextField(blank=True, null=True)),
                ('sent', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthcare.Member')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
