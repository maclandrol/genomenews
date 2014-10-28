# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=10000)),
                ('karma', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentReplyVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.ForeignKey(to='news.CommentReply')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('submitted_date', models.DateTimeField()),
                ('karma', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=10000)),
                ('karma', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostCommentVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.ForeignKey(to='news.PostComment')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.ForeignKey(to='news.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('karma', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='postvote',
            name='voter',
            field=models.ForeignKey(to='news.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postcommentvote',
            name='voter',
            field=models.ForeignKey(to='news.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postcomment',
            name='commenter',
            field=models.ForeignKey(to='news.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postcomment',
            name='target',
            field=models.ForeignKey(to='news.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(to='news.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commentreplyvote',
            name='voter',
            field=models.ForeignKey(to='news.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commentreply',
            name='commenter',
            field=models.ForeignKey(to='news.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commentreply',
            name='root',
            field=models.ForeignKey(to='news.PostComment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commentreply',
            name='target',
            field=models.ForeignKey(blank=True, to='news.CommentReply', null=True),
            preserve_default=True,
        ),
    ]
