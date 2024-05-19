from django.db import models
from .questions import Question
from .answers import Answer
# Create your models here.

class Vote(models.Model):
    '''
    Vote model
    '''
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    vote_type = models.CharField(max_length=1, default="L", choices=[("L", "Like"), ("D", "Dislike")])