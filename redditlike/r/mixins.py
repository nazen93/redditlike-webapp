from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator

from .forms import SearchForm, VotingForm, SignUpForm, MyAuthenticationForm, ModalAutenticationForm, TextPost, LinkPost, CommentRepliesForm
from .models import SubForum, PostText, Voter, UserProfile, Comments, CommentReplies
from message.models import PrivateMessage

from itertools import chain

class GetAuthorMixin:
    """
    Retrieves the post's author.
    """
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(GetAuthorMixin, self).form_valid(form)
    
    
class NewPostSuccessURLMixin:
    
    """
    Gets the success url and redirects to newly created post.
    """
    def get_success_url(self):
        return reverse('detailview', args=(self.object.subforum, self.object.slug))
    
    
class MultipleFormsMixin:
    """
    Adds multiple forms to the context.
    """
    def get_context_data(self, *args, **kwargs):
        context = super(MultipleFormsMixin, self).get_context_data(**kwargs)
        current_user = self.request.user
        if str(current_user) != 'AnonymousUser':
            userprofile_object = UserProfile.objects.get(user=current_user)
            context['subscribed'] = userprofile_object.subscirbed.all()
        context['search_form'] = SearchForm
        context['login_form'] = MyAuthenticationForm
        context['modal_login_form'] = ModalAutenticationForm
        context['register_form'] = SignUpForm
        context['text_post_form'] = TextPost
        context['link_post_form'] = LinkPost
        context['comment_reply_form'] = CommentRepliesForm
        return context
    
class SubscribeMixin:
    """
    Adds variable to the context to check if the current subforum has already been subscribed by the current user.
    """
    def get_context_data(self, *args, **kwargs):
        context = super(SubscribeMixin, self).get_context_data(*args, **kwargs)
        current_user = self.request.user
        category = self.kwargs['category']
        number_of_subscribers = UserProfile.objects.filter(subscirbed__name__contains=category)
        context['number_of_subscribers'] = number_of_subscribers.count() #adds number of subscribers to the context
        if str(current_user) != 'AnonymousUser': #checks if the user is logged in
            userprofile_object = UserProfile.objects.get(user=current_user)
            current_subforum = SubForum.objects.get(name=category)
            if current_subforum in userprofile_object.subscirbed.all(): #checks if the logged in user has already subsribed to the given subforum. if True
                context['already_subscribed'] = True #then adds 'already subsribed' value to the context to display proper form
        return context

 
class UnreadCountMixin:
    '''
    Adds 'unread' variable to the context that contains a number of unread, releated to the logged in user messages/posts/replies.
    '''
    def get_context_data(self, *args, **kwargs):
        context = super(UnreadCountMixin, self).get_context_data(*args, **kwargs)
        current_user = self.request.user
        if str(current_user) != 'AnonymousUser':
            messages_query = PrivateMessage.objects.filter(recipient=current_user, has_read=False).count()
            post_reply_count = Comments.objects.filter(thread__author=current_user, has_read=False).exclude(author=current_user).count() #checks how many unread comments the user has excluding the one posted by the user 
            comment_reply_count = CommentReplies.objects.filter(main_post__author=current_user, has_read=False).exclude(author=current_user).count() #checks how many unread comment replies the user has excluding the one posted by the user
            total_unread = messages_query + post_reply_count + comment_reply_count
            context['unread'] = total_unread
        return context
    
class LoginRequiredMixin:
    """
    Restricts access to not logged in users.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
    

class PreviousPageMixin:
    """
    Redirects to the page at which the form was submitted.
    """            
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER','/')
    
    
class AlreadyLoggedin:
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.success_url)
        else:
            return super(AlreadyLoggedin, self).dispatch(request, *args, **kwargs)