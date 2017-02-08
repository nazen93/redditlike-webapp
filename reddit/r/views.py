from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.views.generic.edit import FormMixin

from .forms import SearchForm, SignUpForm, VotingForm, CommentForm, CommentRepliesForm, MyAuthenticationForm, TextPost, LinkPost
from .mixins import NewPostSuccessURLMixin, GetAuthorMixin, SearchFormMixin, LoginRequiredMixin, PreviousPageMixin, AlreadyLoggedin
from .models import SubForum, PostText, UserProfile, Voter, Comments, CommentReplies
from .voting_class import Voting_function

from io import StringIO
from itertools import chain
from PIL import Image


# Create your views here.

class PostsList(SearchFormMixin, FormMixin, ListView):
    model = PostText
    template_name = "r/basic_index.html"
    form_class = SearchForm
    paginate_by = 20
    context_object_name = 'TextPosts'
    
    def get_queryset(self):        
        form = self.form_class(self.request.GET)
        if form.is_valid():
            search_data = form.cleaned_data['search']
            return PostText.objects.filter(Q(body__icontains = search_data) | Q(title__icontains = search_data))
        else:
            return PostText.objects.order_by('-date')
             
        
class SubredditPostsList(PostsList):
        
    def get_queryset(self):
        category = self.kwargs['category']
        return PostText.objects.filter(subreddit__name=category).order_by('-date')
    
        
class PostView(Voting_function, PreviousPageMixin, SearchFormMixin, FormMixin, DetailView):
    model = PostText
    template_name = "r/post_detail_view.html"
    context_object_name = 'TextPost'
    form_class = CommentForm

    def get_object(self):
        object = super(PostView, self).get_object()
        up_votes = object.up_votes
        down_votes = object.down_votes
        all_votes = up_votes + down_votes
        if all_votes == 0:
            object.average = 0
        else:
            object.average = up_votes/all_votes*100
            object.average = int(object.average)
            if object.average < 0:
                object.average=0                
        return object 
    
    def post(self, request, *args, **kwargs):
        variables = ['slug', 'pk', 'instance', 'direction']
        for variable in variables: 
            if variable not in self.kwargs:
                self.kwargs[variable] = None
        
        slug = self.kwargs['slug']        
        comment_pk = self.kwargs['pk']
        instance = self.kwargs['instance']
        direction = self.kwargs['direction'] 
        
        if comment_pk == None:
            body = self.request.POST['body']
            object = PostText.objects.get(slug=slug)
            form = self.get_form()
            Comments.objects.create(thread_id=object.pk, body=body, author=self.request.user)
            PostText.objects.filter(slug=self.kwargs['slug']).update(comments_count = F('comments_count') +1)   
        elif comment_pk != None and instance != None:
            body = self.request.POST['body']
            instance_level = int(instance)
            comment_object = Comments.objects.get(pk=comment_pk)
            form = self.get_form()
            CommentReplies.objects.create(main_post_id=comment_object.pk, body=body, author=self.request.user, instance=instance_level+1)     
            PostText.objects.filter(slug=self.kwargs['slug']).update(comments_count = F('comments_count') +1)                     
        else:
            form = self.get_form()
            self.voting_function(Comments, CommentReplies)            
            return super(PostView, self).form_valid(form)
              
        if form.is_valid():
            return super(PostView, self).form_valid(form)
        else:
            return super(PostView, self).form_invalid(form)
 
    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data()
        slug = self.kwargs['slug']
        post_object = PostText.objects.get(slug=slug)
        comments = Comments.objects.filter(thread_id=post_object.pk).order_by('date')
        for comment in comments:
            comment.child = CommentReplies.objects.filter(main_post_id=comment.pk)
            for reply in comment.child:
                reply.padding = reply.instance * 25
        context['comments'] = comments
        return context


class NewTextPost(LoginRequiredMixin, SearchFormMixin, GetAuthorMixin, NewPostSuccessURLMixin, CreateView):
    form_class = TextPost
    template_name = 'r/new_text_post.html'
    

class NewLinkPost(NewTextPost):
    form_class = LinkPost
    

class RegisterUser(AlreadyLoggedin, FormView):
    form_class = SignUpForm
    template_name = 'r/new_text_post.html'
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        if self.request.POST['password'] == self.request.POST['password2']:
            user = User.objects.create_user(self.request.POST['username'], self.request.POST['email'], self.request.POST['password'])
            user.save()
            return super(RegisterUser, self).form_valid(form)
        else:
            return super(RegisterUser, self).form_invalid(form)
  
    def get_success_url(self):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterUser, self).get_success_url()
    

class LoginView(AlreadyLoggedin, PreviousPageMixin, SearchFormMixin, FormView):
    form_class = AuthenticationForm
    template_name = 'r/new_text_post.html'
                
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
        return self.request.META.get('HTTP_REFERER','/')
    
        
class Voting(Voting_function, PreviousPageMixin, LoginRequiredMixin, SearchFormMixin, FormView):
    form_class = VotingForm
    template_name = 'r/new_text_post.html'

    def form_valid(self, form):
        self.voting_function(PostText, None)                  
        return super(Voting, self).form_valid(form)
