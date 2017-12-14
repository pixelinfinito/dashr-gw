# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-28 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_deposittransaction_proceeded'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposittransaction',
            name='incoming_dash_transaction_hash',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='deposittransaction',
            name='outgoing_ripple_transaction_hash',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
