from django.contrib import admin
from .models import SubForum, PostText, UserProfile, Comments, CommentReplies, Voter

# Register your models here.

admin.site.register(SubForum)
admin.site.register(PostText)
admin.site.register(UserProfile)
admin.site.register(Comments)
admin.site.register(CommentReplies)
admin.site.register(Voter)