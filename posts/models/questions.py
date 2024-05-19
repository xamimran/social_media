from django.db import models

# Create your models here.

class Question(models.Model):
    '''
    Question model
    '''
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    topics = models.ManyToManyField("Topic")
    popularity = models.IntegerField(default=0)
