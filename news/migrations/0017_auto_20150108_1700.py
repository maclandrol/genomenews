# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0016_auto_20150108_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreply',
            name='owner',
            field=models.ForeignKey(to='news.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commentreplyvote',
            name='voter',
            field=models.ForeignKey(to='news.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='owner',
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
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='userprofile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
