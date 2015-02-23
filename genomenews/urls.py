from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from news.views import UserDetailView, UserEditView
from news.views import PostSubmitView, PostDetailView
from news.views import PostUpdateView, PostDeleteView
from django.contrib.auth.decorators import login_required

# Find admin auto
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'genomenews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'news.views.home', name='home'),
    url(r'^top$', 'news.views.home', name='top'),
    url(r'^newest$', 'news.views.newest', name='newest'),
    url(r'^users/(?P<slug>\w+)/$', UserDetailView.as_view(), name='profile'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name='logout'),
    url(r'^resetpassword/passwordsent/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),
    url(r'^resetpassword/$',
        'django.contrib.auth.views.password_reset',
        name='reset_password'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^register/', 'news.views.registration', name='registration'),

    # User should login before editing his profile
    url(r'edit-profile/$',
        login_required(UserEditView.as_view()),
        name='edit_profile'),
    url(r'^post/(?P<pk>\d+)/$',
        PostDetailView.as_view(),
        name='link_detail'),
    url(r'^post/update/(?P<pk>\d+)/$',
        login_required(PostUpdateView.as_view()),
        name='link_update'),
    url(r'^post/delete/(?P<pk>\d+)/$',
        login_required(PostDeleteView.as_view()),
        name='link_delete'),

    # Post submission form
    url(r'^submit$',
        login_required(PostSubmitView.as_view()),
        name='submit'),
)

urlpatterns += patterns('',
    url(r'^comment/', include('threadedcomment.urls')),
)
