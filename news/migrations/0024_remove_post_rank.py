# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_post_is_self_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='rank',
        ),
    ]
