from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^del/(?P<comment_id>\d+)/$', 'threadedcomment.views.delete_comment', {"template":"comments/comment_delete.html"}, name='comments-delete'),
    url(r'^moderate/(?P<comment_id>\d+)/$', 'threadedcomment.views.delete_comment', {"template":"comments/comment_delete.html", "moderate":True}, name='comments-moderate'),

)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
