from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PrivateMessage(models.Model):
    recipient = models.CharField(max_length=30, verbose_name='to')
    author = models.ForeignKey(User, null=True)
    topic = models.CharField(max_length=120)
    body = models.TextField(verbose_name='message')
    date = models.DateTimeField(auto_now_add=True, null=True)
    has_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.topic
    

        