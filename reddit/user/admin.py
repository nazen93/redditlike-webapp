from django.contrib import admin
from .models import ThreadKarmaPoints, CommentKarmaPoints

# Register your models here.

admin.site.register(ThreadKarmaPoints)
admin.site.register(CommentKarmaPoints)