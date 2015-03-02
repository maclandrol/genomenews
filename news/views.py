from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import DetailView, UpdateView
from django.views.generic import DeleteView, CreateView
from django.db import connection, transaction

from news.models import UserProfile, Post
from news.forms import UserProfileForm, RegistrationForm, PostForm
import news.models as models


def home(request):
    """Website homepage displaying the top posts.

    """
    TOP_POSTS_PER_PAGE = 25

    # TODO: order by rank
    posts = models.Post.objects.all().order_by("-submitted_date")
    posts = posts.order_by('-karma')
    post_in_page = posts[:TOP_POSTS_PER_PAGE]

    return paginate_post(request, posts, TOP_POSTS_PER_PAGE)


def newest(request):
    """Website page displaying the newest posts.

    """
    NEW_POSTS_PER_PAGE = 25

    posts = models.Post.objects.all().order_by("-submitted_date")
    post_in_page = posts[:NEW_POSTS_PER_PAGE]

    return paginate_post(request, posts, NEW_POSTS_PER_PAGE, title="Newest Post | ")


def paginate_post(request, posts, pagination, title=""):
    """Generic view for pagination

    """
    ctx = {}

    paginator = Paginator(posts, pagination)
    page = request.GET.get('page')

    try:
        post_in_page = paginator.page(page)
    except PageNotAnInteger:
        # Display first page then
        post_in_page = paginator.page(1)
    except EmptyPage:
        # Page number is an integer but out of bounds
        # Display first page if user request page 0
        # Otherwise display an empty page
        if(int(page)==0):
            post_in_page = paginator.page(1)
        else:
            post_in_page=[]

    ctx["user"] = request.user
    ctx["posts"] = post_in_page
    ctx["title"] = title

    return render_to_response("home.html", ctx)


def registration(request):
    """Website registration page

    """
    # If user is already logged in, no need to register just redirect to
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
                password=form.cleaned_data["password"]
            )
            user.save()
            userprofile = UserProfile(user=user)
            userprofile.save()
            # Automatically login after registration.
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
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


class PostSubmitView(CreateView):
    """View for post submission.

    """
    model = Post
    form_class = PostForm
    template_name = "post/post_form.html"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.owner = self.request.user.userprofile
        f.save()
        return super(CreateView, self).form_valid(form)

    def get_success_url(self):
        """Success url for the post submission

        The get_absolute_url method of the model should provide
        the success_url. Here we are using a trick to distinct
        self post from link post. We set the url to the full url
        from the get_absolute_url if it's a self post

        """
        success_url = super(PostSubmitView, self).get_success_url()
        post = self.object
        if not post.url:
            post.url = self.request.build_absolute_uri(success_url)
            post.is_self_post = True
            post.save()
        return success_url


class PostDetailView(DetailView):
    """Detail view for a Post

    """
    model = Post
    template_name = "post/post_detail.html"


class PostUpdateView(UpdateView):
    """Post update view

    """
    model = Post
    form_class = PostForm
    template_name = "post/post_form.html"

    def get_queryset(self):
        """User should only modify data he own."""
        qs = super(PostUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class PostDeleteView(DeleteView):
    """View for deleting a post

    """
    model = Post
    template_name = "post/post_delete.html"
    # FIXME: Don't know if redirecting to home after deleting a post
    # is the best way...
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        """ Object can only be deleted by its owner """
        post = super(PostDeleteView, self).get_object()
        if not post.owner == self.request.user:
            raise Http404
        return post
