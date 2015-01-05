from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from news.views import UserDetailView, UserEditView
from django.contrib.auth.decorators import login_required


# Find admin auto
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'genomenews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'news.views.home', name='home'),
    url(r"^users/(?P<slug>\w+)/$", UserDetailView.as_view(), name="profile"),
    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name="logout"),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset', name="reset_password"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^register/', 'news.views.registration', name='registration'),

    # User should login before editing his profile
    url(r"edit_profile/$", login_required(UserEditView.as_view()), name="edit_profile"),
)
