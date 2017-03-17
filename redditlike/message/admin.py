from django.contrib import admin
from .models import PrivateMessage

# Register your models here.

class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'topic', 'date']
    list_filter = ['date']
    search_fields = ['author', 'recipient', 'topic', 'body']
    
    class Meta:
        model = PrivateMessage

admin.site.register(PrivateMessage, PrivateMessageAdmin)