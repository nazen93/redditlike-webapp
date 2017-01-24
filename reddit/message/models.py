from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PrivateMessage(models.Model):
    recipient = models.CharField(max_length=30)
    author = models.ForeignKey(User, null=True)
    topic = models.CharField(max_length=120)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.topic
    

        