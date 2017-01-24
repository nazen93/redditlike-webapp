from django.contrib import admin
from .models import SubForum, PostText, UserProfile, Comments, Voter

# Register your models here.

admin.site.register(SubForum)
admin.site.register(PostText)
admin.site.register(UserProfile)
admin.site.register(Comments)
admin.site.register(Voter)