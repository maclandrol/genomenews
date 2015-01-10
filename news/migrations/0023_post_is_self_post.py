# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0022_post_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_self_post',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
