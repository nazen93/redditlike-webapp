from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.views.generic.edit import FormMixin
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect, HttpResponse
from .models import SubForum, PostText, UserProfile, Voter, Comments
from .forms import SearchForm, SignUpForm, VotingForm, CommentForm, MyAuthenticationForm
from .mixins import NewPostSuccessURLMixin, GetAuthorMixin, SearchFormMixin, LoginRequiredMixin, PreviousPageMixin, AlreadyLoggedin
from io import StringIO
from PIL import Image

from itertools import chain

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
        
    
class Testoriiiino(ListView):
    model = PostText
    template_name = "r/test.html"
    context_object_name = 'TextPosts'
    
    def get_queryset(self):
        pierwsze = PostText.objects.all()
        drugie = Voter.objects.filter(user=self.request.user)
        a = []
        for x in drugie:
            a.append(x.vote_id)
        a = list(set(a))
        wut = PostText.objects.filter(pk__in=a).order_by('-date')
        return wut
                               
        
class SubredditPostsList(PostsList):
        
    def get_queryset(self):
        category = self.kwargs['category']
        return PostText.objects.filter(subreddit__name=category).order_by('-date')
    
        
class PostView(PreviousPageMixin, SearchFormMixin, FormMixin, DetailView):
    model = PostText
    template_name = "r/post_detail_view.html"
    context_object_name = 'TextPost'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        body = self.request.POST['body']
        slug = self.kwargs['slug']
        object = PostText.objects.get(slug=slug)
        form = self.get_form()
        Comments.objects.create(thread_id=object.pk, body=body, author=self.request.user)
        PostText.objects.filter(slug=slug).update(comments_count = F('comments_count') +1)
        if form.is_valid():
            return super(PostView, self).form_valid(form)
        else:
            return super(PostView, self).form_invalid(form)
 
    def get_context_data(self, *args, **kwargs):
        context = super(PostView, self).get_context_data()
        slug = self.kwargs['slug']
        post_object = PostText.objects.get(slug=slug)
        comments = Comments.objects.filter(thread_id=post_object.pk).order_by('date')
        context['comments'] = comments
        return context
    

class NewTextPost(LoginRequiredMixin, SearchFormMixin, GetAuthorMixin, NewPostSuccessURLMixin, CreateView):
    model = PostText
    fields = ['title', 'body', 'subreddit']
    template_name = 'r/new_text_post.html'
    

class NewLinkPost(NewTextPost):
    fields = ['link', 'image', 'title', 'subreddit']
    

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
    
        
class Voting(PreviousPageMixin, LoginRequiredMixin, SearchFormMixin, FormView):
    form_class = VotingForm
    template_name = 'r/new_text_post.html'

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        direction = self.kwargs['direction']
        post_object = PostText.objects.filter(pk=post_pk)
        voter_object = Voter.objects.filter(vote_id=post_pk, user_id=self.request.user.id)
        voter_object_up = Voter.objects.filter(vote_id=post_pk, user_id=self.request.user.id, voting_direction='up')
        voter_object_down = Voter.objects.filter(vote_id=post_pk, user_id=self.request.user.id, voting_direction='down')
        voter_object_none = Voter.objects.filter(vote_id=post_pk, user_id=self.request.user.id, voting_direction='empty')

        if direction == "up" and voter_object_up.exists():      
            post_object.update(rating=F('rating') - 1)
            voter_object.update(voting_direction='empty')
        elif direction =='up' and voter_object_down.exists():
            post_object.update(rating=F('rating') + 2)
            voter_object.update(voting_direction='up')
        elif direction =='up' and voter_object_none.exists():
            post_object.update(rating=F('rating') + 1)
            voter_object.update(voting_direction='up')
        elif direction=="up":
            post_object.update(rating=F('rating') + 1)
            Voter.objects.create(vote_id=post_pk, user_id=self.request.user.id, voting_direction=direction)
        elif direction=='down' and voter_object_up.exists():
            post_object.update(rating=F('rating') - 2)
            voter_object.update(voting_direction='down')
        elif direction=='down' and voter_object_down.exists():
            post_object.update(rating=F('rating') + 1)
            voter_object.update(voting_direction='empty')
        elif direction =='down' and voter_object_none.exists():
            post_object.update(rating=F('rating') - 1)
            voter_object.update(voting_direction='down')
        elif direction=='down':
            post_object.update(rating=F('rating') - 1)
            Voter.objects.create(vote_id=post_pk, user_id=self.request.user.id, voting_direction=direction)
                            
        return super(Voting, self).form_valid(form)
