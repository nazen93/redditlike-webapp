from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from r.mixins import LoginRequiredMixin, GetAuthorMixin
from r.models import PostText, Comments, CommentReplies

from itertools import chain
# Create your views here.

class AllUserPosts(TemplateView):
    template_name = 'user/all_user_posts.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(AllUserPosts, self).get_context_data(*args, **kwargs)
        user = self.kwargs['username']
        user_threads = PostText.objects.filter(author__username=user)
        user_comments = Comments.objects.filter(author__username=user)
        user_replies = CommentReplies.objects.filter(author__username=user)
        combined_list = list(chain(user_threads, user_comments, user_replies))
        combined_list.sort(key=lambda i:i.date, reverse=True)
        context['user'] = user
        context['user_activity'] = combined_list
        return context
    
class UserComments(TemplateView):
    template_name = 'user/all_user_posts.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserComments, self).get_context_data(*args, **kwargs)
        user = self.kwargs['username']
        user_comments = Comments.objects.filter(author__username=user)
        user_replies = CommentReplies.objects.filter(author__username=user)
        combined_list = list(chain(user_comments, user_replies))
        combined_list.sort(key=lambda i:i.date, reverse=True)
        context['user'] = user
        context['user_activity'] = combined_list
        return context
    
class UserThreads(ListView):
    model = PostText
    template_name = 'user/all_user_posts.html'
    context_object_name = 'user_activity'
    
    def get_queryset(self, **kwargs):
        user = self.kwargs['username']
        user_threads = PostText.objects.filter(author__username=user)
        return user_threads
            
    def get_context_data(self, *args, **kwargs):
        context = super(UserThreads, self).get_context_data(*args, **kwargs)
        user = self.kwargs['username']
        context['user'] = user
        return context
    
    