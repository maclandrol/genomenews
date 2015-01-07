# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='karma',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
