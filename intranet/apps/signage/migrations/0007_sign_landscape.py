# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('signage', '0006_sign_zoom')]

    operations = [migrations.AddField(
        model_name='sign',
        name='landscape',
        field=models.BooleanField(default=False),
    )]
