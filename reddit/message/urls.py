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
    url(r'^inbox/$', views.Inbox.as_view(), name='inbox'),
    url(r'^messages/$', views.Messages.as_view(), name='messages'),
    url(r'^mentions/$', views.Mentions.as_view(), name='mentions'),
    url(r'^compose/$', views.SendPM.as_view(), name='compose'),
    url(r'^sent/$', views.Sent.as_view(), name='sent'),
    url(r'^post_replies/$', views.PostReplies.as_view(), name="post_replies"),
    url(r'compose/to=(?P<user>[\w]+)$', views.SenPMTo.as_view(), name='pm'),
]