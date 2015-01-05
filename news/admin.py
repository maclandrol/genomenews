from django.contrib import admin
from news.models import Post, PostComment, UserProfile, PostVote
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


# Register your models here.
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostVote)

# See Customizing authentication in django
# https://docs.djangoproject.com/en/1.7/topics/auth/customizing/
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)
