from django.contrib import admin
from .models import Post, PostComment, User, PostVote
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostVote)
"""
class UserInline(admin.StackedInline):
    model = User
    can_delete = False

class UserAdmin(DjangoUserAdmin):
    inlines=(UserInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
"""
