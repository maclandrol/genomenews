# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentreply',
            old_name='commenter',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='postcomment',
            old_name='commenter',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='post',
            name='submitted_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
