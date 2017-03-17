from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.

class ThreadKarmaPoints(models.Model):
    user = models.ForeignKey(User)
    voter = models.ForeignKey(User, related_name="thread_voters")
    has_voted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.voter.username


class CommentKarmaPoints(models.Model):
    user = models.ForeignKey(User)
    voter = models.ForeignKey(User, related_name="comment_voters")
    has_voted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.voter.username