from threadedcomment.models import ThreadedComment
from threadedcomment.forms import ThreadedCommentForm
from django.core import urlresolvers

def get_model():
    return ThreadedComment

def get_form():
    return ThreadedCommentForm

def get_form_target():
    return urlresolvers.reverse("threadedcomment.views.comment_view")
