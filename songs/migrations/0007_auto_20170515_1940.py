# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-15 19:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0006_alternatebookname_alternativeparshaname'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AlternativeParshaName',
            new_name='AlternateParshaName',
        ),
    ]