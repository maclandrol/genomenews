# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20150103_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='karma',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
