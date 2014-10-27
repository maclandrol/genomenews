
from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    """A user for the website.

    We mostly use Django's default behavior for authentication, but we might
    need to add a little bit of information (e.g. karma and possibly more stuff
    in the future).

    """
    user = models.OneToOneField(User)
    karma = models.IntegerField(default=0)


class Post(models.Model):
    """A Post to the news website.

    This is the atom of the website: it represents either a "self" post where
    users can write questions for the community, or a more standard "link" 
    post where users share web content. Votes and comments will be anchored
    to the posts.

    """
    owner = models.ForeignKey(User)
    title = models.CharField()
    url = models.CharField()
    submitted_date = models.DateTimeField()
    karma = models.IntegerField(default=0)


class Comment(models.Model):
    """Abstract class for comments. 

    """
    commenter = models.ForeignKey(User)
    comment = models.CharField()
    karma = models.IntegerField(default=0)
    class Meta:
        abstract = True


class PostComment(Comment):
    """A comment for a given Post.

    """
    target = models.ForeignKey(Post)


class CommentReply(Comment):
    """A comment for a given comment (reply).

    """
    target = models.ForeignKey(Comment)


class Vote(models.Model):
    """Abstract class for Votes.

    this is subclassed to allow voting ont Posts and on Comments.

    """
    voter = models.ForeignKey(User)

    class Meta:
        abstract = True


class PostVote(Vote):
    """A post vote unit.

    We need to record who voted for what article. Hence, a database entry
    will be added for every vote. This is to avoid re-votes as the score
    will be recorder in the Post to avoid recomputing it at every page load.
    
    """
    target = models.ForeignKey(Post)


class CommentVote(Vote):
    """A comment vote unit.

    """
    target = models.ForeignKey(Comment)


# Utility functions
def karma_inc(o):
    """Increments the karma count for an object.

    This function returns False if the object does not have a karma attribute.

    """
    if hasattr(o, "karma"):
        o.karma += 1
        o.save()
        return True

    else:
        return False

