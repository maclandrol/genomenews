# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20141028_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rank',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='biography',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
