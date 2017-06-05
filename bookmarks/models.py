from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here

class Link(models.Model):
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.url

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user_id = models.ForeignKey(User)
    link_id = models.ForeignKey(Link)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=54, unique = True)
    bookmarks = models.ManyToManyField(Bookmark)

    def __str__(self):
        return self.name

class SharedBookmark(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    date = models.DateTimeField(auto_now_add = True)
    votes = models.IntegerField(default=1)
    users_voted = models.ManyToManyField(User)

    def __str__(self):
        return ("{}-{}".format(self.bookmark, self.votes))

class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name = "from_friend")
    to_friend = models.ForeignKey(User, related_name = "to_friend")

    def __str__(self):
        return ("{} - {}".format(self.from_friend, self.to_friend))

    class meta:
        unique_together = ('to_friend', 'from_friend')
