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
