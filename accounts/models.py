'''
This file is used to create a custom user model.
'''
from django.db import models
from django.contrib.auth.models import AbstractUser

from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    '''
    Custom user model
    '''
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    gender= models.CharField(max_length=10, null=True, blank=True)
    profilePicture = CloudinaryField('image')
    designation = models.CharField(max_length=100, null=True, blank=True)


class Poll(models.Model):
    '''
    Poll model
    '''
    question = models.CharField(max_length=200)

class Option(models.Model):
    '''
    Option model
    '''
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=100)

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_votes')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
