'''
This file contains the answer view.
'''

from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Answer, Vote, Question


class LikeAnswerView(LoginRequiredMixin, View):
    '''
    This class handles the like answer view.
    '''
    def post(self, request, answer_id, *args, **kwargs):
        '''
        This method handles the post request.
        '''
        answer = get_object_or_404(Answer, pk=answer_id)
        user = self.request.user

        # Check if the user has already liked the answer
        existing_vote = Vote.objects.filter(answer=answer, author=user, vote_type='L').first()

        if not existing_vote:
            # If the user hasn't liked the answer, create a new like
            Vote.objects.create(answer=answer, author=user, vote_type='L')

            # if the user has disliked the answer, delete the dislike
            existing_dislike = Vote.objects.filter(answer=answer, author=user, vote_type='D').first()
            if existing_dislike:
                existing_dislike.delete()

        # Redirect back to the question or wherever you want
        return redirect('/home', answer_id=answer_id)

class DislikeAnswerView(LoginRequiredMixin, View):
    '''
    This class handles the dislike answer view.
    '''
    def post(self, request, answer_id, *args, **kwargs):
        '''
        This method handles the post request.
        '''
        answer = get_object_or_404(Answer, pk=answer_id)
        user = self.request.user

        # Check if the user has already disliked the answer
        existing_vote = Vote.objects.filter(answer=answer, author=user, vote_type='D').first()

        if not existing_vote:
            # If the user hasn't disliked the answer, create a new dislike
            Vote.objects.create(answer=answer, author=user, vote_type='D')

            # if the user has liked the answer, delete the like
            existing_like = Vote.objects.filter(answer=answer, author=user, vote_type='L').first()
            if existing_like:
                existing_like.delete()

        # Redirect back to the question or wherever you want
        return redirect('/home', answer_id=answer_id)

class AnswerQuestionView(LoginRequiredMixin, View):
    '''
    This class handles the answer question view.
    '''
    def post(self, request, question_id, *args, **kwargs):
        '''
        This method handles the post request.
        '''
        question = get_object_or_404(Question, pk=question_id)
        user = self.request.user

        # Create a new answer
        Answer.objects.create(question=question, author=user, description=request.POST.get('answer'))


        # Redirect back to the question or wherever you want
        return redirect('/home', question_id=question_id)
