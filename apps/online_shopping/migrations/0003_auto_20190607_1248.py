# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-07 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shopping', '0002_auto_20190607_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additional_img',
            name='image_file',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='prod',
            name='main_img',
            field=models.TextField(),
        ),
    ]
