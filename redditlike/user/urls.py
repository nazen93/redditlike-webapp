from django.conf.urls import url, include
from . import views

# Create your views here.

urlpatterns = [
    url(r'^(?P<username>[\w]+)/$', views.AllUserPosts.as_view(), name="all_activity"),
    url(r'^(?P<username>[\w]+)/comments/$', views.UserComments.as_view(), name="user_comments"),
    url(r'^(?P<username>[\w]+)/submitted/$', views.UserThreads.as_view(), name="user_threads"),    
    ]