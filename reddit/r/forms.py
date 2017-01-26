from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from .models import Comments


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'size': 26,
        'placeholder': 'search'
        }))
    
class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        widgets = {
            'password' : forms.PasswordInput(),
            'password' : forms.PasswordInput()
            } 
        help_texts = {'username': 'Username'}

class VotingForm(forms.Form):
    Vote = forms.BooleanField(required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'size': 13, 
        'placeholder':'username'
    }))    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'size': 13, 'placeholder':'password'
    }))