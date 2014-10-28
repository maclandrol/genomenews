
from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    """A user for the website.

    We mostly use Django's default behavior for authentication, but we might
    need to add a little bit of information (e.g. karma and possibly more stuff
    in the future).

    """
    user = models.OneToOneField(DjangoUser)
    karma = models.IntegerField(default=0)

    def __repr__(self):
        return u"#{} {} ({})".format(self.pk, self.user.username, self.karma)


class Post(models.Model):
    """A Post to the news website.

    This is the atom of the website: it represents either a "self" post where
    users can write questions for the community, or a more standard "link" 
    post where users share web content. Votes and comments will be anchored
    to the posts.

    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    submitted_date = models.DateTimeField(auto_now_add=True)
    karma = models.IntegerField(default=0)

    def upvote(self, user):

        # Add the PostVote to the database.
        pv = PostVote(voter=user, target=self)
        pv.save()


class Comment(models.Model):
    """Abstract class for comments. 

    """
    owner = models.ForeignKey(User)
    comment = models.CharField(max_length=10000)
    karma = models.IntegerField(default=0)
    class Meta:
        abstract = True


class PostComment(Comment):
    """A comment for a given Post.

    """
    target = models.ForeignKey(Post)


class CommentReply(Comment):
    """A comment for a given comment (reply).

    :param root: Always contains a the PostComment which is the first node
                 in the discussion tree.

    :param target: The target comment (for replies). If this is NULL, we
                   assume that this reply is to the root PostComment.

    """
    root = models.ForeignKey(PostComment)
    target = models.ForeignKey("self", blank=True, null=True)


class Vote(models.Model):
    """Abstract class for Votes.

    this is subclassed to allow voting ont Posts and on Comments.

    """
    voter = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        """The save function for Vote objects increases the karma counters.

        """
        # Record the upvote.
        self.target.karma += 1
        self.target.owner.karma += 1

        self.target.save()
        self.target.owner.save()

        super(Vote, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PostVote(Vote):
    """A post vote unit.

    We need to record who voted for what article. Hence, a database entry
    will be added for every vote. This is to avoid re-votes as the score
    will be recorder in the Post to avoid recomputing it at every page load.
    
    """
    target = models.ForeignKey(Post)


class PostCommentVote(Vote):
    """An upvote for the comment of a post.

    """
    target = models.ForeignKey(PostComment)


class CommentReplyVote(Vote):
    """An upvote for the comment of a comment (reply).

    """
    target = models.ForeignKey(CommentReply)

