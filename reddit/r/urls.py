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
from updown.views import AddRatingFromModel
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', views.PostsList.as_view(), name='index'),
    url(r'^test/$', views.Testoriiiino.as_view()),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^(?P<word>[\w]+)/(?P<pk>.*)/vote(?P<direction>(up|down))/$', views.Voting.as_view(), name='voting'),
    url(r'^(?P<word>[\w]+)/(?P<slug>.*)/$', views.PostView.as_view(), name='detailview'),
    url(r'^addpost/$', views.NewTextPost.as_view(), name='new_text_post'),
    url(r'^addlinkpost/$', views.NewLinkPost.as_view(), name='new_link_post'),
    url(r'^register/$', views.RegisterUser.as_view(), name="register"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^(?P<category>[\w]+)/$', views.SubredditPostsList.as_view(), name='category'),
]