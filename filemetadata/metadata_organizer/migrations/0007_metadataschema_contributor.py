# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-29 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata_organizer', '0006_auto_20160427_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadataschema',
            name='contributor',
            field=models.CharField(default='Dataverse core', max_length=255),
        ),
    ]
