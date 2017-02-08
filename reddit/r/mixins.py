from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator

from .forms import SearchForm, VotingForm, SignUpForm, MyAuthenticationForm, ModalAutenticationForm, TextPost, LinkPost, CommentRepliesForm
from .models import PostText, Voter, UserProfile, Comments

class GetAuthorMixin:
    """
    Retrieves the post's author
    """
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(GetAuthorMixin, self).form_valid(form)
    
    
class NewPostSuccessURLMixin:
    
    """
    Gets the success url and redirects to newly created post
    """
    def get_success_url(self):
        return reverse('detailview', args=(self.object.subreddit, self.object.slug))
    
    
class SearchFormMixin:
    """
    Adds SearchForm to the context
    """
    def get_context_data(self, *args, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm
        context['login_form'] = MyAuthenticationForm
        context['modal_login_form'] = ModalAutenticationForm
        context['register_form'] = SignUpForm
        context['text_post_form'] = TextPost
        context['link_post_form'] = LinkPost
        context['comment_reply_form'] = CommentRepliesForm
        return context
    
    
class LoginRequiredMixin:
    """
    Restricts access to not logged in users
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
    

class PreviousPageMixin:
    """
    Redirects to the page at which the form was submitted
    """            
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER','/')
    
    
class AlreadyLoggedin:
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.success_url)
        else:
            return super(AlreadyLoggedin, self).dispatch(request, *args, **kwargs)