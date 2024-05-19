from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Topic(models.Model):
    '''
    Topic model
    '''
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    followed_by = models.ManyToManyField("accounts.CustomUser", related_name="followed_topics")
    topic_picture = CloudinaryField('image', blank=True, null=True)
    topic_date = models.DateTimeField(blank=True, null=True, default=None)
    address = models.CharField(max_length=200, blank=True, null=True)
