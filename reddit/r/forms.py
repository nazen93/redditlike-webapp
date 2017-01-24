from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from .models import Comments

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)
    
class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        widgets = {
            'password' : forms.PasswordInput(),
            'password' : forms.PasswordInput()
            } 

class VotingForm(forms.Form):
    Vote = forms.BooleanField(required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']