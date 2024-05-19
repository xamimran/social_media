'''
This class handles the like question view.
'''

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Question, Topic, Vote
from posts.common.queries import QuestionPageQueries
from django.views import View
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

class QuestoinView(LoginRequiredMixin, TemplateView):
    '''
    This class handles the specific question view.
    '''
    template_name = "posts/templates/question.html"

    def get_context_data(self, **kwargs):
        '''
        This method handles the get request.
        '''
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        context["question"] = QuestionPageQueries.get_complete_question(question)
        context["topics"] = Topic.objects.all()
        return context

class AddQuestionView(LoginRequiredMixin, TemplateView):
    '''
    This class handles the add question view.
    '''
    template_name = "posts/templates/add_question.html"

    def get_context_data(self, **kwargs):
        '''
        This method handles the get request.
        '''
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        '''
        This method handles the post request.
        '''
        title = request.POST.get("title")
        description = request.POST.get("description")
        author = request.user

        # Create a new question
        question = Question.objects.create(
            title=title,
            description=description,
            author=author,
        )

        # Handle topics
        topic_id = request.POST.get("topic")

        # if topic id is -1 and user is business, no need to add topic, also 
        # set the popularity of question to 5
        if topic_id == "-1" and request.user.designation == "business":
            question.popularity = 5
            question.save()
            return redirect("profile")


        if topic_id:
            topic = Topic.objects.get(pk=topic_id)
            question.topics.add(topic)  
            
        return redirect("topic_page", topic_id=topic_id)
    
class AddQuestionFormView(LoginRequiredMixin, TemplateView):
    '''
    This class handles the add question form view.
    '''
    template_name = "posts/templates/add_question.html"

    def get_context_data(self, **kwargs):
        '''
        This method handles the get request.
        '''
        context = super().get_context_data(**kwargs)
        all_questions = QuestionPageQueries.get_all_questions()
        paginator = Paginator(all_questions, 10)  # Show 10 questions per page

        page = self.request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            questions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            questions = paginator.page(paginator.num_pages)

        context["all_questions"] = questions
        context["topics"] = Topic.objects.all()
        return context
    
class LikeQuestionView(LoginRequiredMixin, View):
    '''
    This class handles the like question view.
    '''
    def post(self, request, question_id, *args, **kwargs):
        '''
        This method handles the post request.
        '''
        question = get_object_or_404(Question, pk=question_id)
        user = self.request.user

        # Check if the user has already liked the question
        existing_vote = Vote.objects.filter(question=question, author=user, vote_type='L').first()

        if not existing_vote:
            # If the user hasn't liked the question, create a new like
            Vote.objects.create(question=question, author=user, vote_type='L')

            # if the user has disliked the question, delete the dislike
            existing_dislike = Vote.objects.filter(question=question, author=user, vote_type='D').first()
            if existing_dislike:
                existing_dislike.delete()

        # Redirect back to the question or wherever you want
        return redirect('/home', question_id=question_id)

class DislikeQuestionView(LoginRequiredMixin, View):
    '''
    This class handles the dislike question view.
    '''
    def post(self, request, question_id, *args, **kwargs):
        '''
        This method handles the post request.
        '''
        question = get_object_or_404(Question, pk=question_id)
        user = self.request.user

        # Check if the user has already disliked the question
        existing_vote = Vote.objects.filter(question=question, author=user, vote_type='D').first()

        if not existing_vote:
            # If the user hasn't disliked the question, create a new dislike
            Vote.objects.create(question=question, author=user, vote_type='D')

            # if the user has liked the question, delete the like
            existing_like = Vote.objects.filter(question=question, author=user, vote_type='L').first()
            if existing_like:
                existing_like.delete()

        # Redirect back to the question or wherever you want
        return redirect('/home', question_id=question_id)
