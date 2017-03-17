from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from .models import PostText, Comments, CommentReplies


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={
        'placeholder': 'search'
        }))
    
class TextPost(forms.ModelForm):
    
    class Meta:
        model = PostText
        fields = ['title', 'body', 'subforum']
    

class LinkPost(forms.ModelForm):
    
    class Meta:
        model = PostText
        fields = ['link', 'image', 'title', 'subforum']
    
class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'id': 'register-form',
        'placeholder': 'verify password',
        'size': 7,
    }))
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        labels = {
            'username': '',
            'email': '',
            'password': '',
            'password2': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'register-form',
                'placeholder': 'username',
        }),                   
            'password': forms.PasswordInput(attrs={
                'id': 'register-form',
                'placeholder': 'password',
        }),                  
            'email': forms.TextInput(attrs={
                'id': 'register-form',
                'placeholder': 'email',
        }),
            } 

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password1 != password2:
            self.add_error('password2', 'The password does not match the first one.')
        
        return cleaned_data


class VotingForm(forms.Form):
    Vote = forms.BooleanField(required=False)
    
class CommentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['placeholder'] = 'type your comment here'
    
    class Meta:
        model = Comments
        fields = ['body']
       

class CommentRepliesForm(forms.ModelForm):
    
    class Meta:
        model = CommentReplies
        fields = ['body']


class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'id': 'login-form',
        'placeholder':'username'
    }))    
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'id': 'login-form',
        'placeholder':'password'
    }))
    
  
class ModalAutenticationForm(MyAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(ModalAutenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['id'] = 'modal-login-form'        
        self.fields['password'].widget.attrs['id'] = 'modal-login-form'
   
