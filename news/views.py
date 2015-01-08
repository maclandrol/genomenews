from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import DetailView, UpdateView
from django.db import connection, transaction

from news.models import UserProfile
from news.forms import UserProfileForm, RegistrationForm
import news.models as models


def reset(request):
    """Reset.

    TODO: Add documentation.

    There is probably a better way of doing this. It seems like it increments
    the internal sequence for the automatic primary keys. Why would the reset
    function do this?

    """
    cursor = connection.cursor()
    cursor.execute("SELECT setval('news_userprofile_id_seq', (SELECT MAX(id) FROM news_userprofile)+1)")
    success = simplejson.dumps({'success':'success',})
    return HttpResponse(success, mimetype='application/json')


def home(request):
    """Website homepage displaying the top posts.

    """
    ctx = {}

    posts = models.Post.objects.all().order_by("-submitted_date")
    posts = posts.order_by('-karma')[:25]
    ctx["posts"] = posts
    ctx["user"] = request.user

    return render_to_response("home.html", ctx)


def registration(request):
    """Website registration page

    """
    # If used is already logged in, no need to register just redirect to
    # the user's profile page.
    if request.user.is_authenticated():
        return HttpResponseRedirect(
            reverse("profile", kwargs={"slug": request.user})
        )
    # If the user is submitting the Registration form.
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"])
            user.save()
            userprofile = UserProfile(user=user)
            userprofile.save()
            # Automatically login after registration.
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            # TODO: Add information on why the form didn't validate.
            return render_to_response(
                "registration.html",
                {"form": form},
                context_instance=RequestContext(request)
            )
    else:
        # User wants to get the registration form.
        form = RegistrationForm()
        ctx = {"form": form}
        return render_to_response(
            "registration.html",
            ctx,
            context_instance=RequestContext(request)
        )


class UserDetailView(DetailView):
    """View for user profiles.

    Displays basic information such as the username, account creation date,
    karma, biography, and email.

    """
    model = get_user_model()
    slug_field = "username"
    template_name = "profile.html"

    def get_object(self, queryset=None):
        user = super(UserDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user


class UserEditView(UpdateView):
    """View to update user profiles.

    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})
