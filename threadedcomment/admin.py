from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ungettext
from django.contrib.comments.admin import CommentsAdmin

from threadedcomment.models import ThreadedComment
from threadedcomment.views import perform_approve, perform_moderation, perform_delete

class ThreadedCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'comment')}
        ),
        (_('Hierarchy'),
           {'fields': ('parent',)}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_deleted', 'is_moderated')}
        ),
    )

    list_display = ('name', 'content_type', 'object_pk', 'id', 'parent',
                    'ip_address', 'submit_date', 'is_public', 'is_deleted', 'is_moderated')
    search_fields = ('comment', 'user__username', 'user_name', 'ip_address')
    raw_id_fields = ("parent",)
    actions = ["flag_comments", "approve_comments", "delete_comments", "moderate_comments"]


    def moderate_comments(self, request, queryset):
        self._bulk_flag(request, queryset, perform_moderation,
                        lambda n: ungettext('moderated', 'moderated', n))
    moderate_comments.short_description = _("Moderate selected comments")

    def approve_comments(self, request, queryset):
        self._bulk_flag(request, queryset, perform_approve,
                        lambda n: ungettext('approved', 'approved', n))
    approve_comments.short_description = _("Approve selected comments")

    def delete_comments(self, request, queryset):
        self._bulk_flag(request, queryset, perform_delete,
                        lambda n: ungettext('deleted', 'deleted', n))
    delete_comments.short_description = _("Remove selected comments (mod)")

    def get_actions(self, request):
        actions = super(CommentsAdmin, self).get_actions(request)
        # Only superusers should be able to delete the comments from the DB.
        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')
        if not request.user.has_perm('threadedcomment.can_moderate'):
            if 'approve_comments' in actions:
                actions.pop('approve_comments')
            if 'moderate_comments' in actions:
                actions.pop('moderate_comments')
        return actions

    def _bulk_flag(self, request, queryset, action, done_message):
        """
        Flag, approve, or remove some comments from an admin action. Actually
        calls the `action` argument to perform the heavy lifting.
        """
        n_comments = 0
        for comment in queryset:
            action(request, comment)
            n_comments += 1

        msg = ungettext('1 comment was successfully %(action)s.',
                        '%(count)s comments were successfully %(action)s.',
                        n_comments)
        self.message_user(request, msg % {'count': n_comments, 'action': done_message(n_comments)})

admin.site.register(ThreadedComment, ThreadedCommentsAdmin)
