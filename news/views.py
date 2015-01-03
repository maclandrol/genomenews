from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import get_user_model
from .models import User
from .forms import UserProfileForm
from django.core.urlresolvers import reverse

import news.models

def home(request):
    """Website homepage displaying the top posts.

    """
    ctx = {}

    posts = news.models.Post.objects.all().order_by("-submitted_date")
    posts = posts.order_by('-rank')[:25]
    ctx["posts"] = posts

    return render_to_response("home.html", ctx)


class UserDetail(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "profile.html"

    def get_object(self, queryset=None):
        user = super(UserDetail, self).get_object(queryset)
        User.objects.get_or_create(user=user)
        return user


class UserEdit(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return User.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})
