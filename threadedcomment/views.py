from __future__ import absolute_import

from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

import django.contrib.comments as django_comment
from django.contrib.comments import signals
from django.contrib.comments.views.comments import CommentPostBadRequest
from django.contrib.comments.views.utils import next_redirect, confirmation_view
from django.core.urlresolvers import reverse
from threadedcomment import get_model_target
from django.shortcuts import redirect

@csrf_protect
def comment_view(request, next=None, using=None, object_pk=None, ctype=None, comment_id=None, templates=None):
    """
    Post a comment.

    HTTP POST is not necessary required. If there are errors an error template,
     ``comments/comment_error.html``, will be rendered.
    On HTTP GET, we the model and id are requered

    """
    # The current comment to render in a detailcomment view
    curcomment = None
    if(comment_id is not None):
        try:
            curcomment = django_comment.get_model()._default_manager.using(using).get(pk=comment_id)
        except ObjectDoesNotExist:
            return CommentPostBadRequest(
                "No object matching your comment %r " % (comment_id))
        except :
            return CommentPostBadRequest(
                "Could not get the target object for your comment: %r " % (comment_id))

    if request.method == "POST":
        return post_comment(request, next, using, object_pk, ctype, curcomment, templates)
    else:
        return get_comment_form(request, next, using, object_pk, ctype, curcomment, templates)

@csrf_protect
@require_POST
def post_comment(request, next=None, using=None, object_pk=None, ctype=None, curcomment=None, templates=None):
    """Post a comment.

    """

    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    # if user is not already authenticated, redirect to login
    if not request.user.is_authenticated():
        # and after login, redirect here again
        return redirect('/login/?next=%s' % data.get("next"))

    if not data.get('name', ''):
        data["name"] = request.user.get_full_name() or request.user.get_username()

    if  (ctype is None or object_pk is None) and curcomment is None:
        return CommentPostBadRequest("Missing content_type, object_pk or comment_id field.")

    # we got the ctype and object_pk but not comment_id
    if curcomment is None:
        try:
            model = models.get_model(*ctype.split(".", 1))
            target = model._default_manager.using(using).get(pk=object_pk)
        except TypeError:
            return CommentPostBadRequest(
                "Invalid content_type value: %r" % escape(ctype))
        except AttributeError:
            return CommentPostBadRequest(
                "The given content-type %r does not resolve to a valid model." % \
                    escape(ctype))
        except ObjectDoesNotExist:
            return CommentPostBadRequest(
                "No object matching content-type %r and object PK %r exists." % \
                    (escape(ctype), escape(object_pk)))
        except (ValueError, ValidationError) as e:
            return CommentPostBadRequest(
                "Attempting go get content-type %r and object PK %r exists raised %s" % \
                    (escape(ctype), escape(object_pk), e.__class__.__name__))

    else :
        target =  curcomment.content_object

    # Construct the comment form
    form = django_comment.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    # If the form is valide,  create the comment
    if form.is_valid():
        comment = form.get_comment_object()
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        comment.user = request.user

        # Signal that the comment is about to be saved
        responses = signals.comment_will_be_posted.send(
            sender=comment.__class__,
            comment=comment,
            request=request
        )

        for (receiver, response) in responses:
            if response == False:
                return CommentPostBadRequest(
                    "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

        # Save the comment and signal that it was saved
        comment.save()
        signals.comment_was_posted.send(
            sender=comment.__class__,
            comment=comment,
            request=request
        )
        return next_redirect(request, fallback=next or 'comments-comment-done',
            c=comment._get_pk_val())

    else :
        ctx = {
            "comment": form.data.get("comment", curcomment),
            "form": form,
            "post": target,
            "object_pk": object_pk,
            "ctype": ctype,
            "next": data.get("next", next),
        }

        return render_to_response(
                templates,
                ctx,
                RequestContext(request, {})
            )


@csrf_protect
@require_GET
def get_comment_form(request, next=None, using=None, object_pk=None, ctype=None, curcomment=None, templates=None):
    """Request the comment by a get request
    This also assure that refreshing the error page or the detailcomment
    won't let to an http 405 error
    """
    # this is a request.GET call
    ctype = request.GET.get("ctype")
    object_pk = request.GET.get("object_pk")

    if  (ctype is None or object_pk is None) and curcomment is None:
        return CommentPostBadRequest("Missing content_type, object_pk or comment_id field.")

    # we got the ctype and object_pk but not comment_id
    if curcomment is None:
        try:
            model = models.get_model(*ctype.split(".", 1))
            target = model._default_manager.using(using).get(pk=object_pk)
        except TypeError:
            return CommentPostBadRequest(
                "Invalid content_type value: %r" % escape(ctype))
        except AttributeError:
            return CommentPostBadRequest(
                "The given content-type %r does not resolve to a valid model." % \
                    escape(ctype))
        except ObjectDoesNotExist:
            return CommentPostBadRequest(
                "No object matching content-type %r and object PK %r exists." % \
                    (escape(ctype), escape(object_pk)))
        except (ValueError, ValidationError) as e:
            return CommentPostBadRequest(
                "Attempting go get content-type %r and object PK %r exists raised %s" % \
                    (escape(ctype), escape(object_pk), e.__class__.__name__))

    else :
        target =  curcomment.content_object

    # we are sending a new clean comment form
    form = django_comment.get_form()(target)
    ctx = {
        "form": form,
        "comment" : curcomment,
        "post": target,
        "object_pk": object_pk,
        "ctype": ctype,
        "next": get_model_target(object_pk) if curcomment is None else None,
    }


    return render_to_response(
            templates,
            ctx,
            RequestContext(request, {})
        )


def edit_comment():
    pass

comment_done = confirmation_view(
    template="comments/posted.html",
    doc="""Display a "comment was posted" success page."""
)
