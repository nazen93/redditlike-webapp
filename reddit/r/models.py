from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

from .imgur_thumbnail import ImgurThumbnail

from io import StringIO, BytesIO
import io
from PIL import Image
from random import randrange
from _sqlite3 import IntegrityError

# Create your models here.

class SubForum(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class PostText(ImgurThumbnail, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50,null=True, editable=False, unique=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_promoted = models.BooleanField(default=False)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)
    rating = models.IntegerField(default=0, editable=False)
    author = models.ForeignKey(User, null=True, editable=False)
    comments_count = models.IntegerField(default=0, editable=False)
    subreddit = models.ForeignKey(SubForum)        

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
            slug_counter = PostText.objects.filter(slug__startswith=self.slug, slug__endswith=self.slug).count()
            if slug_counter != 0:
                self.slug = '%s-%s' % (self.slug, str(slug_counter))
                
                                       
        if self.image:  
            self.body = self.thumbnail_file((255,255))
            self.image.file = self.thumbnail_file((55,55))
            
        if self.link and 'imgur' in self.link:
            picture_path = self.download_thumbnail(self.link)
            fullsize_picture_path = self.imgur_thumbnail(self.link)            
            self.body = self.imgur_image_large(fullsize_picture_path)
            self.image = picture_path
            
        super(PostText, self).save(*args, **kwargs)
                 
    def __str__(self):
        return self.title
    

class Comments(models.Model):
    thread = models.ForeignKey(PostText, related_name='comments')
    body = models.TextField('')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, editable=False)
    rating = models.IntegerField(default=0, editable=False)
    voted = models.ForeignKey('Voter', null=True)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)
    default_instance = models.IntegerField(default=0)

    def __str__(self):
        return self.body

class CommentReplies(models.Model):
    main_post = models.ForeignKey(Comments, null=True)
    body = models.TextField('', null=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, editable=False)
    voted = models.ForeignKey('Voter', null=True)
    rating = models.IntegerField(default=0, editable=False)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)
    instance = models.IntegerField(default=0, editable=False)
    
    def __str__(self):
        return self.body
 

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
