"""reddot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.PostsList.as_view(), name='index'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^submit/$', views.NewTextPost.as_view(), name='new_text_post'),
    url(r'^submit-link/$', views.NewLinkPost.as_view(), name='new_link_post'),
    url(r'^register/$', views.RegisterUser.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^random/$', views.RandomSubforum.as_view(), name='random'),
    url(r'^close/(?P<pk>[0-9]+)/$', views.CloseThread.as_view(), name='close'),
    url(r'^(?P<sorting>(new|top|controversial|rising|promoted))/$', views.SortedPostsList.as_view(), name='sorting'),
    url(r'^(?P<category>[\w]+)/$', views.CategoryPostsList.as_view(), name='category'),
    url(r'^(?P<category>[\w]+)/(?P<action>(subscribe|unsubscribe))/$', views.SubscribeCategory.as_view(), name='subscribe'),
    url(r'^(?P<category>[\w]+)/(?P<sorting>(new|top|controversial|rising|promoted))/$', views.SortedSubforumList.as_view(), name='subforum_sorting'),
    url(r'^(?P<word>[\w]+)/(?P<pk>[0-9]+)/vote(?P<direction>(up|down))/$', views.Voting.as_view(), name='voting'),
    url(r'^(?P<word>[\w]+)/(?P<slug>[^/]+)/$', views.PostView.as_view(), name='detailview'),
    url(r'^(?P<word>[\w]+)/(?P<slug>[^/]+)/(?P<pk>[0-9]+)/post/$', views.PostUpdate.as_view(), name='update_post'),
    url(r'^(?P<word>[\w]+)/(?P<slug>[^/]+)/(?P<pk>[0-9]+)/comment/$', views.CommentUpdate.as_view(), name='update_comment'),
    url(r'^(?P<word>[\w]+)/(?P<slug>[^/]+)/(?P<pk>[0-9]+)/reply/$', views.ReplyUpdate.as_view(), name='update_reply'),
    url(r'^(?P<word>[\w]+)/(?P<slug>[^/]+)/(?P<pk>[0-9]+)/(?P<instance>[0-9]+)/$', views.PostView.as_view(), name='comment_reply'),
    url(r'^(?P<word>[\w]+)/(?P<slug>[^/]+)/(?P<pk>[0-9]+)/vote(?P<direction>(up|down))/$', views.PostView.as_view(), name='comment_voting'),
]