# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-13 00:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shopping', '0003_auto_20190607_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]