from threadedcomment.models import ThreadedComment
from threadedcomment.forms import ThreadedCommentForm
from django.core import urlresolvers

def get_model():
    return ThreadedComment

def get_form():
    return ThreadedCommentForm

def get_form_target():
    return urlresolvers.reverse("postcomment")

def get_model_target(object_pk):
    return urlresolvers.reverse("link_detail", kwargs={"pk":object_pk})
