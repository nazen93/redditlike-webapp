from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.urls import reverse, reverse_lazy 
from django.views.generic import TemplateView, ListView, CreateView

from r.extra import VotedUpDown
from r.mixins import LoginRequiredMixin, GetAuthorMixin
from r.models import PostText, Comments, CommentReplies
from .forms import PrivateMessageForm
from .models import PrivateMessage

from itertools import chain

# Create your views here.

class Inbox(VotedUpDown, LoginRequiredMixin, ListView):
    model = PostText
    template_name = 'message/inbox.html'
    paginate_by = 20
    context_object_name = 'inbox'
    
    def get_queryset(self, **kwargs):
        user = self.request.user
        messages_query = PrivateMessage.objects.filter(recipient=user)
        post_reply_query = Comments.objects.filter(thread__author=user).exclude(author=user)
        comment_reply_query = CommentReplies.objects.filter(main_post__author=user).exclude(author=user)
        messages_query.update(has_read=True) #updates the unread messages(has_read) to True
        post_reply_query.update(has_read=True) #updates the unread post replies(has_read) to True
        comment_reply_query.update(has_read=True) #updates the unread comment replies (has_read) to True
        combined_query = list(chain(messages_query, post_reply_query, comment_reply_query)) #combines the querysets
        updated_queryset = self.up_or_down(combined_query)
        updated_queryset.sort(key=lambda i:i.date, reverse=True) #sorts the combined queryset by date
        return updated_queryset 

            
class Messages(LoginRequiredMixin, ListView):
    model = PrivateMessage
    template_name = "message/messages.html"
    context_object_name = 'Messages'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        return PrivateMessage.objects.filter(recipient=user).order_by('-date')
    
    
class Sent(Messages):
    template_name = "message/sent.html"
    
    def get_queryset(self):
        user = self.request.user
        return PrivateMessage.objects.filter(author=user).order_by('-date')
    
class PostReplies(VotedUpDown, Messages):
    template_name = "message/post_replies.html"
    
    def get_queryset(self):
        user = self.request.user
        queryset = Comments.objects.filter(thread__author=user).exclude(author=user).order_by('-date')
        updated_queryset = self.up_or_down(queryset)
        return updated_queryset
    
    
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
        

    