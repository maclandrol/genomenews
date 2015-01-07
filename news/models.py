from django.db import models
from urlparse import urlparse
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.db.models import F
from math import log10



class UserProfile(models.Model):
    """A user for the website.

    We mostly use Django's default behavior for authentication, but we might
    need to add a little bit of information (e.g. karma and possibly more stuff
    in the future).

    """
    user = models.OneToOneField(User, unique=True)
    karma = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add extra attribute : user bio
    biography = models.TextField(null=True)


    def __repr__(self):
        return u"#{} {} ({})\nAbout:\n{}".format(self.pk, self.user.username,
                                                 self.karma, self.biography)


    def __unicode__(self):
        """UserProfile representation

        """

        return "%s" % self.user


class Post(models.Model):
    """A Post to the news website.

    This is the atom of the website: it represents either a "self" post where
    users can write questions for the community, or a more standard "link"
    post where users share web content. Votes and comments will be anchored
    to the posts.

    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    submitted_date = models.DateTimeField(auto_now_add=True)
    rank = models.FloatField(default=0.0)
    karma = models.IntegerField(default=0)

    def upvote(self, user):
        # Add the PostVote to the database.
        pv = PostVote(voter=user, target=self)
        pv.save()

    def domain(self):
        """Returns the domain of the url.

        """
        parsed_url = urlparse(self.url)
        # get the domain name. This will keep the top level domain name
        domain='{uri.netloc}'.format(uri=parsed_url)
        # remove subdomain www if it persists and convert to lowercase
        return domain.lower().strip("www.")

    def comment_count(self):
        """Returns the number of PostComment instances that have this post as their target.

        """
        return len(PostComment.objects.filter(target=self))

    def set_rank(self):
        """Hacker news ranking algorithm
        see http://amix.dk/blog/post/19574

        """
        SECS_IN_HOUR=float(3600)
        GRAVITY=1.5
        delta= now() - self.submitted_date
        post_age = delta.total_seconds() // SECS_IN_HOUR
        self.rank = ((self.karma-1) / pow(post_age+2, GRAVITY))
        self.save()

    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"pk": str(self.id)})

    def __unicode__(self):
        return self.title

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

    this is subclassed to allow voting on Posts and on Comments.

    """
    voter = models.ForeignKey(User)


    def save(self, *args, **kwargs):
        """The save function for Vote objects increases the karma counters.

        """
        # Record the upvote.
        # self.target.update(karma=F('karma') + 1)
        # self.target.owner.userprofile.update(karma=F('karma') + 1)

        self.target.karma += 1
        self.target.owner.userprofile.karma += 1
        self.target.save()
        self.target.owner.userprofile.save()

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


# This is a signal to connect user to userprofile.
# Because I'm already using a registration system,
# this is useless and generate errors
'''
def create_profile_callback(sender, instance, created, **kwargs):
    """Callback to save userprofile

    """
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile_callback, sender=User)
'''
