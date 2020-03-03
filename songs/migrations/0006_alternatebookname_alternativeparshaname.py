# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-15 19:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0005_auto_20170502_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternateBookName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternate_name', models.CharField(max_length=256, null=True)),
                ('book_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songs.BookName')),
            ],
        ),
        migrations.CreateModel(
            name='AlternativeParshaName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternate_name', models.CharField(max_length=256, null=True)),
                ('parsha_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songs.ParshaName')),
            ],
        ),
    ]