# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-27 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parshaname',
            name='prefix',
            field=models.CharField(default='00', max_length=4),
            preserve_default=False,
        ),
    ]
