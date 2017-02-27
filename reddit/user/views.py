from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .mixins import UserDataMixin

from .models import ThreadKarmaPoints, CommentKarmaPoints
from r.extra import VotedUpDown
from r.mixins import LoginRequiredMixin, GetAuthorMixin, SearchFormMixin
from r.models import PostText, Comments, CommentReplies

from itertools import chain
# Create your views here.

class AllUserPosts(SearchFormMixin, VotedUpDown, UserDataMixin, ListView):
    model = PostText
    template_name = 'user/all_user_posts.html'
    paginate_by = 20
    context_object_name = 'user_activity'
    
    def get_queryset(self, **kwargs):
        current_user = self.kwargs['username']
        user_threads = PostText.objects.filter(author__username=current_user)
        user_comments = Comments.objects.filter(author__username=current_user)
        user_replies = CommentReplies.objects.filter(author__username=current_user)
        combined_list = list(chain(user_threads, user_comments, user_replies))
        combined_list.sort(key=lambda i:i.date, reverse=True)
        updated_queryset = self.up_or_down(combined_list)
        return updated_queryset
    
class UserComments(AllUserPosts):
    
    def get_queryset(self, **kwargs):
        current_user = self.kwargs['username']
        user_comments = Comments.objects.filter(author__username=current_user)
        user_replies = CommentReplies.objects.filter(author__username=current_user)
        combined_list = list(chain(user_comments, user_replies))
        combined_list.sort(key=lambda i:i.date, reverse=True)
        updated_queryset = self.up_or_down(combined_list)
        return updated_queryset
    
class UserThreads(AllUserPosts):
    
    def get_queryset(self, **kwargs):
        current_user = self.kwargs['username']
        user_threads = PostText.objects.filter(author__username=current_user)
        updated_queryset = self.up_or_down(user_threads)
        return updated_queryset

    
    