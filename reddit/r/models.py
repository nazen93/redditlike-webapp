from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from .imgur_thumbnail import ImgurThumbnail
from io import StringIO, BytesIO
import io
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

# Create your models here.

class SubForum(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class PostText(ImgurThumbnail, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50,null=True, editable=False)
    link = models.URLField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, editable=False)
    author = models.ForeignKey(User, null=True, editable=False)
    voted = models.ForeignKey('Voter', null=True)
    subreddit = models.ForeignKey(SubForum)        

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)            
        if self.image:
            picture_path = self.image
            picture_file = BytesIO(picture_path.read())
            picture = Image.open(picture_file)
            
            picture.thumbnail((55,55), Image.ANTIALIAS)
            picture_file = BytesIO()
            picture.save(picture_file, 'JPEG')
            
            picture_path.file = picture_file  
                    
        if self.link and 'imgur' in self.link:
            picture_path = self.download_thumbnail(self.imgur_thumbnail, self.link, self.imgur_imageid)
            self.image = picture_path
        
        return super(PostText, self).save(*args, **kwargs)               

    def __str__(self):
        return self.title

class Comments(models.Model):
    thread = models.ForeignKey(PostText, related_name='comments')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, editable=False)

    def __str__(self):
        return str(self.thread)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(PostText, null=True)

    
    def __str__(self):
        return str(self.user)

class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.ForeignKey(PostText, on_delete=models.CASCADE)
    voting_direction = models.CharField(max_length=10, null=True)
    
    def __str__(self):
        return str(self.voting_direction)
   
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
            
post_save.connect(create_user_profile, sender=User)
