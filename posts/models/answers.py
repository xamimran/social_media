from django.db import models
from .questions import Question
# Create your models here.

class Answer(models.Model):
    '''
    Answer model
    '''
    description = models.TextField()
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
