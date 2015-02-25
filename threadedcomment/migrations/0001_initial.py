# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadedComment',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='comments.Comment')),
                ('tree_path', models.TextField(verbose_name='Tree path', editable=False, db_index=True)),
                ('duplicate', models.BooleanField(default=False, verbose_name='Duplicate')),
                ('karma', models.IntegerField(default=0, verbose_name='karma')),
                ('last_child', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Last child', blank=True, to='threadedcomment.ThreadedComment', null=True)),
                ('parent', models.ForeignKey(related_name='children', default=None, blank=True, to='threadedcomment.ThreadedComment', null=True, verbose_name='Parent')),
            ],
            options={
                'ordering': ('tree_path',),
                'db_table': 'threadedcomments_comment',
                'verbose_name': 'Threaded comment',
                'verbose_name_plural': 'Threaded comments',
            },
            bases=('comments.comment',),
        ),
    ]
