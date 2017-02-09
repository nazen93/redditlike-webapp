from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.urls import reverse, reverse_lazy 
from django.views.generic import TemplateView, ListView, CreateView

from r.mixins import LoginRequiredMixin, GetAuthorMixin
from r.models import PostText, Comments
from .forms import PrivateMessageForm
from .models import PrivateMessage

from itertools import chain

# Create your views here.

class Inbox(LoginRequiredMixin, TemplateView):
    template_name = 'message/inbox.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Inbox, self).get_context_data(*args, **kwargs)
        user = self.request.user
        messages_query = PrivateMessage.objects.filter(recipient=user)
        post_query = Comments.objects.filter(thread__author=user)
        #post_query = PostText.objects.filter(Q(body__icontains=user) | Q(title__icontains=user))
        comment_query = Comments.objects.filter(body__icontains=user)
        combined_query = list(chain(messages_query, post_query, comment_query))
        combined_query.sort(key=lambda i:i.date, reverse=True)
        context['inbox'] = combined_query
        return context
    
        
class Messages(LoginRequiredMixin, ListView):
    model = PrivateMessage
    template_name = "message/messages.html"
    context_object_name = 'Messages'
    
    def get_queryset(self):
        user = self.request.user
        return PrivateMessage.objects.filter(recipient=user).order_by('-date')
    
class Sent(Messages):
    template_name = "message/sent.html"
    
    def get_queryset(self):
        user = self.request.user
        return PrivateMessage.objects.filter(author=user).order_by('-date')
    
class PostReplies(Messages):
    template_name = "message/post_replies.html"
    
    def get_queryset(self):
        user = self.request.user
        return Comments.objects.filter(thread__author=user).order_by('-date')
    
    
class Mentions(LoginRequiredMixin, ListView):
    model = PostText
    template_name = "message/mentions.html"
    context_object_name = 'Mentions'
    
    def get_queryset(self):
        mentioned_user = '@'+str(self.request.user)
        post_query = PostText.objects.filter(Q(body__icontains=mentioned_user) | Q(title__icontains=mentioned_user))
        comment_query = Comments.objects.filter(body__icontains=mentioned_user)
        combined_query = list(chain(post_query, comment_query))
        combined_query.sort(key=lambda i:i.date, reverse=True)
        return combined_query
    
    
class SendPM(LoginRequiredMixin, GetAuthorMixin, CreateView):    
    form_class = PrivateMessageForm
    success_url = reverse_lazy('index')
    template_name = 'message/compose_pm.html'
    
    def get_form_kwargs(self):
        kwargs = super(SendPM, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
                    

class SenPMTo(SendPM):
    
    def get_initial(self):
        recipient = self.kwargs['user']     
        return {'recipient' : recipient}
        

    