from django.conf.urls import url, include
from . import views
from updown.views import AddRatingFromModel
from django.views.generic.base import RedirectView

# Create your views here.

urlpatterns = [
    url(r'^register/$', views.RegisterUser.as_view(), name="register"),
    ]