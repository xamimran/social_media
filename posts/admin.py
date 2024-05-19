from django.contrib import admin

# Register your models here.
from .models.questions import Question
from .models.answers import Answer
from .models.topics import Topic
from .models.votes import Vote

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Topic)
admin.site.register(Vote)
