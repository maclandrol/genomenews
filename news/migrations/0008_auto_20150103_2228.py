# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20150103_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='karma',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
