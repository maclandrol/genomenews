from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from news.views import UserDetail, UserEdit
from django.contrib.auth.decorators import login_required


# Find admin auto
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'genomenews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'news.views.home', name='home'),
    url(r"^users/(?P<slug>\w+)/$", UserDetail.as_view(), name="profile"),
    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name="logout"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r"edit_profile/$", login_required(UserEdit.as_view()), name="edit_profile")


)
