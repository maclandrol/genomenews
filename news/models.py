from math import log10
from urlparse import urlparse

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.db.models import F
from threadedcomment.models import ThreadedComment


class UserProfile(models.Model):
    """A user for the website.

    We mostly use Django's default behavior for authentication, but we might
    need to add a little bit of information (e.g. karma and possibly more stuff
    in the future).

    """

    user = models.OneToOneField(User, unique=True, related_name="userprofile")
    karma = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add extra attribute: user bio
    biography = models.TextField(null=True)

    def __repr__(self):
        return u"#{} {} ({})".format(self.pk, self.user.username, self.karma)

    def __unicode__(self):
        """UserProfile representation. """
        return self.user.username


class Post(models.Model):
    """A Post to the news website.

    This is the atom of the website: it represents either a "self" post where
    users can write questions for the community, or a more standard "link"
    post where users share web content. Votes and comments will be anchored
    to the posts.

    """
    owner = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    submitted_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    karma = models.IntegerField(default=0)
    is_self_post = models.BooleanField(default=False)

    def upvote(self, user):
        # Add the PostVote to the database.
        pv = PostVote(voter=user, target=self)
        pv.save()

    def domain(self):
        """Returns the domain of the url.

        """
        parsed_url = urlparse(self.url)
        # get the domain name. This will keep the top level domain name
        domain = '{uri.netloc}'.format(uri=parsed_url)
        # remove subdomain www if it persists and convert to lowercase
        return domain.lower().strip("www.") if not self.is_self_post else ""

    def rank(self):
        """Hacker news ranking algorithm.

        see http://amix.dk/blog/post/19574
        """
        SECS_IN_HOUR = 3600.0
        GRAVITY = 1.5

        delta = now() - self.submitted_date
        post_age = delta.total_seconds() // SECS_IN_HOUR
        return ((self.karma - 1) / (post_age + 2) ** GRAVITY)

    def get_absolute_url(self):
            return reverse("link_detail", kwargs={"pk": str(self.id)})

    def __unicode__(self):
        return self.title

class Vote(models.Model):
    """Abstract class for Votes.

    this is subclassed to allow voting on Posts and on Comments.

    """
    voter = models.ForeignKey(UserProfile)

    def save(self, *args, **kwargs):
        """The save function for Vote objects increases the karma counters.

        """
        # Record the upvote.
        # self.target.update(karma=F('karma') + 1)
        # self.target.owner.userprofile.update(karma=F('karma') + 1)

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


class CommentVote(Vote):
    """An upvote for the comment of a post.
    """
    target = models.ForeignKey(ThreadedComment)
