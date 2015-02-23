from django.contrib import admin
from django.utils.translation import ugettext_lazy as utl
from django.contrib.comments.admin import CommentsAdmin

from threadedcomment.models import ThreadedComment

class ThreadedCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (utl('Content'),
           {'fields': ('user', 'user_name', 'comment')}
        ),
        (utl('Hierarchy'),
           {'fields': ('parent',)}
        ),
        (utl('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
    )

    list_display = ('name', 'content_type', 'object_pk', 'parent',
                    'ip_address', 'submit_date', 'is_public', 'is_removed')
    search_fields = ('comment', 'user__username', 'user_name', 'ip_address')
    raw_id_fields = ("parent",)

admin.site.register(ThreadedComment, ThreadedCommentsAdmin)
