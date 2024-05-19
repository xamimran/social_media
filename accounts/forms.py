'''
This file is used to create a custom form for the user model.
'''

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    '''
    Custom user creation form
    '''
    class Meta(UserCreationForm):
        '''
        Meta class for the custom user creation form
        '''
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("gender", "age", "email", "profilePicture", "first_name", "last_name", "designation")


class CustomUserChangeForm(UserChangeForm):
    '''
    Custom user change form
    '''
    class Meta:
        '''
        Meta class for the custom user change form
        '''
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class PollForm(forms.Form):
    '''
    Form for creating a poll
    '''
    question = forms.CharField(label='Poll Question', max_length=200)
    options = forms.CharField(label='Poll Options', widget=forms.Textarea)
