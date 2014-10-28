
from django.shortcuts import render_to_response
from django.http import HttpResponse

import news.models

def home(request):
    """Website homepage displaying the top posts.

    """
    ctx = {}

    posts = news.models.Post.objects.all().order_by("-submitted_date")
    posts = posts.order_by('-karma')[:25]
    ctx["posts"] = posts

    return render_to_response("home.html", ctx)

