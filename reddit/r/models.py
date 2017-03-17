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
    has_read = models.BooleanField(default=False)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)
    rating = models.IntegerField(default=0, editable=False)
    author = models.ForeignKey(User, null=True, editable=False)
    comments_count = models.IntegerField(default=0, editable=False)
    subforum = models.ForeignKey(SubForum)        

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
            slug_counter = PostText.objects.filter(slug__istartswith=self.slug).count() #checks how many threads start with the same slug
            if slug_counter != 0: #if slug name is not unique
                self.slug = '%s-%s' % (self.slug, str(slug_counter)) #new slug is created consisting the original slug and the slug counter
                                                     
        if self.image:  
            self.body = self.thumbnail_file((255,255)) #creates a body image from a file that was uploaded
            self.image.file = self.thumbnail_file((55,55)) #creates a thumbnail from the file that was uploaded
            
        if self.link and 'imgur' in self.link: #checks if the provided url contains imgur 
            picture_path = self.download_thumbnail(self.link) #creates a thumbnail from the link that was provided
            fullsize_picture_path = self.imgur_thumbnail(self.link) #receives a direct link to the image
            self.body = self.imgur_image_large(fullsize_picture_path) #sets large imgur thumbnail as body content of the post
            self.image = picture_path #sets resized image as a thumbnail
            
        super(PostText, self).save(*args, **kwargs)
                 
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'    

class Comments(models.Model):
    thread = models.ForeignKey(PostText, related_name='comments')
    body = models.TextField('')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, editable=False)
    rating = models.IntegerField(default=0, editable=False)
    voted = models.ForeignKey('Voter', null=True)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)
    has_read = models.BooleanField(default=False)
    default_instance = models.IntegerField(default=0)

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'   

class CommentReplies(models.Model):
    main_post = models.ForeignKey(Comments, null=True)
    body = models.TextField('', null=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, editable=False)
    voted = models.ForeignKey('Voter', null=True)
    rating = models.IntegerField(default=0, editable=False)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)
    has_read = models.BooleanField(default=False)
    instance = models.IntegerField(default=0, editable=False)
    
    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Comment reply'
        verbose_name_plural = 'Comment replies'    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(PostText, null=True)
    subscirbed = models.ManyToManyField(SubForum, blank=True, related_name='subscription_list')    
    
    def __str__(self):
        return self.user.username

    
class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.ForeignKey(PostText, on_delete=models.CASCADE)
    voting_direction = models.CharField(max_length=10, null=True)
    
    def __str__(self):
        return self.voting_direction
   
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
            
post_save.connect(create_user_profile, sender=User)
