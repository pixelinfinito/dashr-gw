# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-23 14:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170607_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ripple_address', models.CharField(max_length=35, validators=[django.core.validators.RegexValidator('^r[rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz]{27,35}$', message='The Ripple address is not valid.')])),
                ('dash_address', models.CharField(max_length=35)),
                ('proceeded', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
