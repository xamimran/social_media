'''
This file contains all the queries that are used in the accounts app.
'''

from accounts.models import CustomUser
from posts.models import Question, Answer, Topic, Vote

class ProfileQueries:
    '''
    This class contains all the queries related to the Profile model.
    '''
    # return the likes and dislikes of the question
    @staticmethod
    def get_votes(question):
        '''
        This method returns the number of likes and dislikes of the question.
        '''
        likes = Vote.objects.filter(question=question, vote_type="L").count()
        dislikes = Vote.objects.filter(question=question, vote_type="D").count()
        return likes, dislikes

    # return the likes and dislikes of the answer
    @staticmethod
    def get_votes_answers(answer):
        '''
        This method returns the number of likes and dislikes of the answer.
        '''
        likes = Vote.objects.filter(answer=answer, vote_type="L").count()
        dislikes = Vote.objects.filter(answer=answer, vote_type="D").count()
        return likes, dislikes

    @staticmethod
    def get_user_by_id(user_id):
        '''
        This method returns the user with the given id.
        '''
        return CustomUser.objects.get(id=user_id)

    @staticmethod
    def all_questions(user_id):
        '''
        This method returns all the questions asked by the user with the given id.
        '''

        data_set = Question.objects.filter(author=user_id)
        likes = 0
        dislikes = 0

        for question in data_set:
            likes, dislikes = ProfileQueries.get_votes(question)
            question.likes = likes
            question.dislikes = dislikes
        return data_set , likes, dislikes

    @staticmethod
    def all_answers(user_id):
        '''
        This method returns all the answers given by the user with the given id.
        '''
        data_set = Answer.objects.filter(author=user_id)

        likes = 0
        dislikes = 0

        for answer in data_set:
            likes, dislikes = ProfileQueries.get_votes_answers(answer)
            answer.likes = likes
            answer.dislikes = dislikes
        return data_set

    @staticmethod
    def all_topics(user_id):
        '''
        This method returns all the topics followed by the user with the given id.
        '''
        return Topic.objects.filter(followed_by=user_id)

    @staticmethod
    def all_votes(user_id):
        '''
        This method returns all the votes given by the user with the given id.
        '''
        return Vote.objects.filter(author=user_id)
