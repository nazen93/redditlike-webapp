from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.views.generic.edit import FormMixin

from .extra import VotedUpDown, Sorting
from .forms import SearchForm, SignUpForm, VotingForm, CommentForm, CommentRepliesForm, MyAuthenticationForm, TextPost, LinkPost
from .mixins import SubscribeMixin, NewPostSuccessURLMixin, GetAuthorMixin, MultipleFormsMixin, LoginRequiredMixin, PreviousPageMixin, AlreadyLoggedin, UnreadCountMixin
from .models import SubForum, PostText, UserProfile, Voter, Comments, CommentReplies
from .voting_class import VotingClass

from datetime import date, datetime, timezone
from io import StringIO
from itertools import chain
from PIL import Image
from random import randrange, choice


# Create your views here.

class PostsList(UnreadCountMixin, VotedUpDown, MultipleFormsMixin, FormMixin, ListView):
    model = PostText
    template_name = "r/basic_index.html"
    form_class = SearchForm
    paginate_by = 20
    context_object_name = 'TextPosts'
    
    def get_queryset(self):        
        form = self.form_class(self.request.GET)
        if form.is_valid():
            search_data = form.cleaned_data['search']
            all_objects = PostText.objects.filter(Q(body__icontains = search_data) | Q(title__icontains = search_data)) #returns a queryset of posts that contain the searched value either in title or inside the body
            updated_queryset = self.up_or_down(all_objects) #checks if the logged in user has already voted for any of the given posts
            return updated_queryset
        else:
            all_objects = PostText.objects.filter(is_active=True).order_by('-rating', '-comments_count')
            updated_queryset = self.up_or_down(all_objects) 
            return updated_queryset
        

class SortedPostsList(Sorting, PostsList):     
    
    def get_queryset(self, **kwargs):
        sorting = self.kwargs['sorting']
        sort_result = self.sort_method(sorting, None) #sorts the queryset by the given sorting method
        return sort_result
    
    def get_context_data(self, *args, **kwargs):
        context = super(SortedPostsList, self).get_context_data(*args, **kwargs)
        sorting = self.kwargs['sorting']
        context['sorting'] = sorting
        return context
            
              
class CategoryPostsList(SubscribeMixin, Sorting, PostsList):
        
    def get_queryset(self):
        category = self.kwargs['category']
        category_or_404 = get_list_or_404(PostText.objects.order_by('-rating', '-comments_count'), subforum__name=category) #checks if the requested subforum exists, if False then it displays HTTP 404 
        updated_queryset = self.up_or_down(category_or_404)
        return updated_queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryPostsList, self).get_context_data(*args, **kwargs)
        subforum_name = self.kwargs['category']
        context['subforum'] = subforum_name #adds subforum variable to the context.
        return context        


class SortedSubforumList(CategoryPostsList):
    
    def get_queryset(self, **kwargs):
        category = self.kwargs['category']
        sorting = self.kwargs['sorting']
        sort_result = self.sort_method(sorting, category)
        return sort_result
    
    def get_context_data(self, *args, **kwargs):
        context = super(SortedSubforumList, self).get_context_data(*args, **kwargs)
        sorting = self.kwargs['sorting']
        context['sorting'] = sorting
        return context


class RandomSubforum(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        all_subforums = SubForum.objects.all()
        randomed_subforum = choice(all_subforums)
        return reverse('category', kwargs={'category' : randomed_subforum})
        

class SubscribeCategory(PreviousPageMixin, CreateView):
    model = UserProfile
    template_name = "r/basic_index.html"
    fields = ['subscirbed']
    
    def form_valid(self, form):
        current_user = self.request.user
        action = self.kwargs['action']
        category = self.kwargs['category']
        userprofile_object = UserProfile.objects.get(user=current_user)
        subforum = SubForum.objects.get(name=category)
        if action == "subscribe":
            userprofile_object.subscirbed.add(subforum) #adds given subforum to UserProfile.subscribed field
        else:
            userprofile_object.subscirbed.remove(subforum) #removes given subforum to UserProfile.subscribed field 
                   
        return HttpResponseRedirect(self.get_success_url())

            
class PostView(UnreadCountMixin, VotedUpDown, VotingClass, PreviousPageMixin, MultipleFormsMixin, FormMixin, DetailView):
    model = PostText
    template_name = "r/post_detail_view.html"
    context_object_name = 'TextPost'
    form_class = CommentForm

    def get_object(self):
        object = super(PostView, self).get_object()
        try:
            user = self.request.user
            unread_post_replies = Comments.objects.filter(thread__author=user, has_read=False).exclude(author=user) #query that contains post replies that have not been read by the author yet
            unread_comment_replies = CommentReplies.objects.filter(main_post__author=user, has_read=False).exclude(author=user) #query that contains comment replies that have not been read by the author yet
            unread_post_replies.update(has_read=True) #updates the queryset's atrribute 'has_read' to True
            unread_comment_replies.update(has_read=True)
            
            if Voter.objects.filter(user=user, vote_id=object.pk, voting_direction="up").exists():
                object.direction = 'up'
            elif Voter.objects.filter(user=user, vote_id=object.pk, voting_direction="down").exists():
                object.direction = 'down'
        except TypeError:
            pass
        
        up_votes = object.up_votes
        down_votes = object.down_votes
        all_votes = up_votes + down_votes
        if all_votes == 0: #if the thread has no votes yet
            object.average = 0 #its value is set to 0
        else:
            object.average = up_votes/all_votes*100
            object.average = int(object.average) #adds positive votes to all votes ratio
            if object.average < 0:
                object.average = 0                
                
        return object 
    
    def post(self, request, *args, **kwargs):
        variables = ['slug', 'pk', 'instance', 'direction']
        for variable in variables: #itterates through the given variables in the url
            if variable not in self.kwargs: #if the given variable is not present in the url(kwargs)
                self.kwargs[variable] = None #variable is set to None to prevent KeyError 
        
        slug = self.kwargs['slug']        
        comment_pk = self.kwargs['pk']
        instance = self.kwargs['instance']
        direction = self.kwargs['direction'] 
        
        if comment_pk == None: #if comment_pk is equal to None, then the POST request contains data about main comment
            body = self.request.POST['body']
            object = PostText.objects.get(slug=slug)
            form = self.get_form()
            Comments.objects.create(thread_id=object.pk, body=body, author=self.request.user)
            PostText.objects.filter(slug=slug).update(comments_count = F('comments_count') +1)   
        elif comment_pk != None and instance != None: #if comment_pk is not equal to None and instance is also different than None, then the POST request contains data about comment reply
            body = self.request.POST['body']
            instance_level = int(instance)
            comment_object = Comments.objects.get(pk=comment_pk)
            form = self.get_form()
            CommentReplies.objects.create(main_post_id=comment_object.pk, body=body, author=self.request.user, instance=instance_level+1)     
            PostText.objects.filter(slug=slug).update(comments_count = F('comments_count') +1)                     
        else: #POST request contains data about voting
            form = self.get_form()
            self.voting_function(Comments, CommentReplies)            
            return super(PostView, self).form_valid(form)
              
        if form.is_valid():
            return super(PostView, self).form_valid(form)
        else:
            return super(PostView, self).form_invalid(form)
 
    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data()
        user = self.request.user
        if str(user) == 'AnonymousUser': #checks if the user is logged in
            user = None
        slug = self.kwargs['slug']
        post_object = PostText.objects.get(slug=slug)
        comments = Comments.objects.filter(thread_id=post_object.pk).order_by('date')
        for comment in comments:
            if Voter.objects.filter(user=user, vote_id=comment.pk, voting_direction="up").exists():
                comment.direction = 'up'
            elif Voter.objects.filter(user=user, vote_id=comment.pk, voting_direction="down").exists():
                comment.direction = 'down'  
            comment.child = CommentReplies.objects.filter(main_post_id=comment.pk).order_by('date')
            for reply in comment.child:
                if Voter.objects.filter(user=user, vote_id=reply.pk, voting_direction="up").exists():
                    reply.direction = 'up'
                elif Voter.objects.filter(user=user, vote_id=reply.pk, voting_direction="down").exists():
                    reply.direction = 'down'  
                reply.margin = reply.instance * 25 #adds extra margin per comment instance

        context['comments'] = comments
        return context


class PostUpdate(UpdateView):
    model = PostText
    fields = ['body']
    template_name = "r/update.html"
	
    def dispatch(self, request, *args, **kwargs):
        current_user = self.request.user
        object = self.get_object()
        if str(current_user) != 'AnonymousUser' and current_user == object.author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
		
class CommentUpdate(PostUpdate):
    model = Comments
    

class ReplyUpdate(PostUpdate): 
    model = CommentReplies
    

class CloseThread(PreviousPageMixin, UpdateView):
    model = PostText
    fields = ['is_active']
    template_name = "r/basic_index.html"
    
    def form_valid(self, form):
        current_user = self.request.user
        thread_pk = self.kwargs['pk']
        thread_object = PostText.objects.get(pk=thread_pk)
        form = self.get_form()
        if current_user == thread_object.author: #checks if the user that is attempting to close the thread is its author 
            thread_object.is_active = False
            thread_object.save()
            if form.is_valid():
                return super(CloseThread, self).form_valid(form)
        else:
            return super(CloseThread, self).form_invalid(form)

       
class NewTextPost(LoginRequiredMixin, MultipleFormsMixin, GetAuthorMixin, NewPostSuccessURLMixin, CreateView):
    form_class = TextPost
    template_name = 'r/new_text_post.html'


class NewLinkPost(NewTextPost):
    form_class = LinkPost
    

class RegisterUser(MultipleFormsMixin, AlreadyLoggedin, FormView):
    form_class = SignUpForm
    template_name = 'r/register.html'
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        user = User.objects.create_user(self.request.POST['username'], self.request.POST['email'], self.request.POST['password'])
        user.save()
        return super(RegisterUser, self).form_valid(form)
  
    def get_success_url(self):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password) 
        login(self.request, user) #automatically logs in the new user
        return super(RegisterUser, self).get_success_url()
    

class LoginView(AlreadyLoggedin, PreviousPageMixin, MultipleFormsMixin, FormView):
    form_class = MyAuthenticationForm
    template_name = 'r/login.html'
                
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)
        
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)
        
        
class LogoutView(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return self.request.META.get('HTTP_REFERER','/') #redirects to previously visited URL
    
        
class Voting(VotingClass, PreviousPageMixin, LoginRequiredMixin, MultipleFormsMixin, FormView):
    form_class = VotingForm
    template_name = 'r/new_text_post.html'

    def form_valid(self, form):
        self.voting_function(PostText, None)                  
        return super(Voting, self).form_valid(form)
