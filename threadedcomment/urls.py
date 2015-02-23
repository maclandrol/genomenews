from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', include('django.contrib.comments.urls')),
    url(r'^$', 'threadedcomment.views.post_comment', name='postcomment'),
    url(r'^(?P<pk>\d+)/$','threadedcomment.views.post_comment', name='detailcomment' )

)
