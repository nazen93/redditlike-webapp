from django.contrib import admin
from .models import SubForum, PostText, UserProfile, Comments, CommentReplies, Voter

# Register your models here.

class PostTextAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'date', 'is_active', 'rating']
    list_filter = ['date', 'is_active', 'rating']
    list_editable = ['is_active']
    search_fields = ['title', 'slug', 'body', 'link']
    
    class Meta:
        model = PostText

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['author', 'body', 'date', 'rating']
    list_filter = ['date', 'rating']
    search_fields = ['author', 'body', 'thread']
    
    class Meta:
        model = Comments

class CommentRepliesAdmin(CommentsAdmin):
    
    class Meta:
        model = CommentReplies
 
class SubForumAdmin(admin.ModelAdmin): 
    list_display = ['name']
    search_fields = ['name']
    
    class Meta:
        model = SubForum
        
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
    filter_horizontal = ['subscirbed']
    
    class Meta:
        model = UserProfile
    
admin.site.register(PostText, PostTextAdmin)
admin.site.register(SubForum, SubForumAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(CommentReplies, CommentRepliesAdmin)
