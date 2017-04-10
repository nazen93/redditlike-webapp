from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from .models import PrivateMessage

class PrivateMessageForm(forms.ModelForm):    
    
    class Meta:
        model = PrivateMessage
        fields = ['recipient','topic', 'body']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PrivateMessageForm, self).__init__(*args,**kwargs) 
        self.fields['body'].widget.attrs['rows'] = 10
    
    def clean_recipient(self):
        recipient = self.cleaned_data.get('recipient')
        current_user = self.user.username
    
        if recipient == current_user:
            raise forms.ValidationError("You can't send a messeage to youself.")
        
        elif not User.objects.filter(username=recipient).exists():
            raise forms.ValidationError('User %s does not exist' % recipient)
        
        elif recipient == None or recipient == "":
            raise forms.ValidationError('Enter a username.')
                             
        return recipient
