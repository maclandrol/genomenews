# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_auto_20150108_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreplyvote',
            name='voter',
            field=models.ForeignKey(to='news.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postcommentvote',
            name='voter',
            field=models.ForeignKey(to='news.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postvote',
            name='voter',
            field=models.ForeignKey(to='news.UserProfile'),
            preserve_default=True,
        ),
    ]
