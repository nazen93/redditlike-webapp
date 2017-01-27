from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from .models import Comments


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={
        'size': 38,
        'placeholder': 'search'
        }))
    
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
        

class VotingForm(forms.Form):
    Vote = forms.BooleanField(required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
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
        self.fields['username'].widget.attrs = {
        'id': 'modal-login-form',
        'placeholder': 'username'
        }
        self.fields['password'].widget.attrs = {
        'id': 'modal-login-form',
        'placeholder': 'password'
        }
   