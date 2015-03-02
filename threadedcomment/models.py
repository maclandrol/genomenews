from django.db import models, transaction, connection
from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager
from django.conf import settings
from django.utils.translation import ugettext_lazy as utl
from django.utils import timezone

PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)

class ThreadedCommentManager(CommentManager):
    def filter(self, *args, **kwargs):
        "small optimization"
        return CommentManager.filter(self, *args, **kwargs).select_related("user")


class ThreadedComment(Comment):
    parent = models.ForeignKey('self', null=True, blank=True, default=None, related_name='children', verbose_name=utl('Parent'))
    last_child = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=utl('Last child'))
    tree_path = models.TextField(utl('Tree path'), editable=False, db_index=True)
    duplicate = models.BooleanField(utl('Duplicate'), default=False)
    is_moderated = models.BooleanField(utl('Moderated'), default=False)
    # django_comment is_removed field fuck-up the template rendering pagination
    # so we are going to add a custom is_deleted field 
    is_deleted = models.BooleanField(utl('Deleted'), default=False)
    objects = ThreadedCommentManager()
    karma = models.IntegerField(utl('karma'), default=0)

    @property
    def depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))

    @property
    def root_id(self):
        return int(self.tree_path.split(PATH_SEPARATOR)[0])

    @property
    def root_path(self):
        return ThreadedComment.objects.filter(pk__in=self.tree_path.split(PATH_SEPARATOR)[:-1])

    def upvote(self, user):
        CommentVoteModel = get_vote_model()
        if CommentVoteModel is not None:
            pv = CommentVoteModel(voter=user, target=self)
            pv.save()

    def save(self, *args, **kwargs):
        skip_tree_path = kwargs.pop('skip_tree_path', False)
        super(ThreadedComment, self).save(*args, **kwargs)
        if skip_tree_path:
            return None

        tree_path = unicode(self.pk).zfill(PATH_DIGITS)
        if self.parent:
            tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

            self.parent.last_child = self
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=self)

        self.tree_path = tree_path
        ThreadedComment.objects.filter(pk=self.pk).update(tree_path=self.tree_path)




    def delete(self, *args, **kwargs):
        # Fix last child on deletion.
        if self.parent_id:
            try:
                prev_child_id = ThreadedComment.objects \
                                .filter(parent=self.parent_id) \
                                .exclude(pk=self.pk) \
                                .order_by('-submit_date') \
                                .values_list('pk', flat=True)[0]
            except IndexError:
                prev_child_id = None
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=prev_child_id)
        super(ThreadedComment, self).delete(*args, **kwargs)

    class Meta(object):
        ordering = ('tree_path',)
        db_table = 'threadedcomments_comment'
        verbose_name = utl('Threaded comment')
        verbose_name_plural = utl('Threaded comments')
