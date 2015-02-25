from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^del/(?P<comment_id>\d+)/$', 'django.contrib.comments.views.moderation.delete',name='comments-delete'),
    url(r'^deleted/$', 'django.contrib.comments.views.moderation.delete_done',  name='comments-delete-done'),
)
urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
