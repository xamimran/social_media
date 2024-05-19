'''
This file contains all the queries that are used in the posts app.
'''
from posts.models import Question, Answer, Vote, Topic
from accounts.models import CustomUser
from django.core.paginator import Paginator


class HomePageQueries:
    '''
    This class contains all the queries that are used in the home page.
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
    def get_all_user_questions(user):
        '''
        This method returns all the questions of the topics the user is following.
        Along with the likes and dislikes of the question.
        Order the questions by number of likes.
        '''
        topics = user.followed_topics.all()
        # don't fetch duplicates questions and topics
        questions = Question.objects.filter(topics__in=topics).distinct()
        questions_list = []
        for question in questions:
            likes, dislikes = HomePageQueries.get_votes(question)
            question.likes = likes
            question.dislikes = dislikes

            # add the answers of the question and their likes and dislikes
            answers = Answer.objects.filter(question=question)

            answers_list = []
            
            for answer in answers:
                likes, dislikes = HomePageQueries.get_votes_answers(answer)
                answer.likes = likes
                answer.dislikes = dislikes
                answers_list.append(answer)

            # sort the answers by number of likes
            answers_list.sort(key=lambda x: x.likes, reverse=True)

            # take only the first two answers
            answers_list = answers_list[:2]

            question.answers = answers_list

            # add the question to the list
            questions_list.append(question)
                    

        questions_list.sort(key=lambda x: x.likes, reverse=True)

        return questions_list

    @staticmethod
    def get_user_questions(user):
        '''
        Use the all questions method to get all the questions of the user.
        each question should have only two answers.
        '''
        questions = HomePageQueries.get_all_user_questions(user)

        for question in questions:
            question.answers = question.answers[:2]

        return questions
    

    @staticmethod
    def get_user_answers(user):
        '''
        This method returns all the answers of the questions the user is following.
        ALong with the likes and dislikes of the answer.
        Order the answers by number of likes.
        '''
        questions = HomePageQueries.get_user_questions(user)
        answers_list = []
        for question in questions:
            answers = Answer.objects.filter(question=question)
            for answer in answers:
                likes, dislikes = HomePageQueries.get_votes(answer)
                answer.likes = likes
                answer.dislikes = dislikes
                answers_list.append(answer)

        answers_list.sort(key=lambda x: x.likes, reverse=True)

        return answers_list



    @staticmethod
    def get_searched_questions(search_str):
        '''
        This method returns all the questions that match the search query.
        Use difflib to get the closest matches.
        '''
        # Get all the questions
        questions = Question.objects.all()

        # Get the questions that match the search query
        questions_list = []
        for question in questions:
            if search_str.lower() in question.title.lower() \
                or search_str.lower() in question.description.lower():
                questions_list.append((question))

        for question in questions_list:
            likes, dislikes = HomePageQueries.get_votes(question)
            question.likes = likes
            question.dislikes = dislikes

            # add the answers of the question and their likes and dislikes
            answers = Answer.objects.filter(question=question)

            answers_list = []

            i = 0
            for answer in answers:
                likes, dislikes = HomePageQueries.get_votes_answers(answer)
                answer.likes = likes
                answer.dislikes = dislikes
                answers_list.append(answer)
                i += 1
                if i == 2:
                    break

            # sort the answers by number of likes
            answers_list.sort(key=lambda x: x.likes, reverse=True)

            question.answers = answers_list[:2]

        questions_list.sort(key=lambda x: x.likes, reverse=True)

        # Search of the topics that match the search query
        topics = Topic.objects.filter(name__icontains=search_str)

        return questions_list, topics
    
    @staticmethod
    def get_all_popular_questions():
        '''
        This method returns all the questions that are popular.
        A question is popular if it has more than 10 likes.
        '''
        questions = Question.objects.filter(popularity__gt=0)
        questions_list = list(questions)
        questions_list.sort(key=lambda x: x.popularity, reverse=True)

        # likes and dislikes
        for question in questions_list:
            likes, dislikes = HomePageQueries.get_votes(question)
            question.likes = likes
            question.dislikes = dislikes

            # add the answers of the question and their likes and dislikes
            answers = Answer.objects.filter(question=question)

            answers_list = []
            
            for answer in answers:
                likes, dislikes = HomePageQueries.get_votes_answers(answer)
                answer.likes = likes
                answer.dislikes = dislikes
                answers_list.append(answer)

            # sort the answers by number of likes
            answers_list.sort(key=lambda x: x.likes, reverse=True)

            # take only the first two answers
            answers_list = answers_list[:2]

            question.answers = answers_list

            

        return questions_list
    
    
class QuestionPageQueries:
    '''
    This class contains all the queries that are used in the question page.
    '''
    @staticmethod
    def get_question_answers(question):
        '''
        This method returns all the answers of the question.
        '''
        answers = Answer.objects.filter(question=question)
        return answers

    @staticmethod
    def get_complete_question(question):
        '''
        This method returns the question along with the answers and their likes and dislikes.
        '''
        answers = QuestionPageQueries.get_question_answers(question)
        for answer in answers:
            likes, dislikes = HomePageQueries.get_votes_answers(answer)
            answer.likes = likes
            answer.dislikes = dislikes
        question.answers = answers
        return question
    
    @staticmethod
    def get_all_questions():
        '''
        This method returns all the questions along with their likes and dislikes.
        Also sort the questions by number of likes.
        Also add the answers of the question and their likes and dislikes.
        '''
        questions = Question.objects.all()
        for question in questions:
            likes, dislikes = HomePageQueries.get_votes(question)
            question.likes = likes
            question.dislikes = dislikes

            # add the answers of the question and their likes and dislikes
            answers = Answer.objects.filter(question=question)

            answers_list = []
            
            for answer in answers:
                likes, dislikes = HomePageQueries.get_votes_answers(answer)
                answer.likes = likes
                answer.dislikes = dislikes
                answers_list.append(answer)

            # sort the answers by number of likes
            answers_list.sort(key=lambda x: x.likes, reverse=True)

            # take only the first two answers
            answers_list = answers_list[:2]

            question.answers = answers_list

        questions_list = list(questions)

        # sort the questions by number of likes
        questions_list.sort(key=lambda x: x.likes, reverse=True)

        return questions_list

class TopicPageQueries:
    '''
    This class contains all the queries that are used in the topic page.
    '''
    @staticmethod
    def get_topic_questions(topic):
        '''
        This method returns all the questions of the topic.
        Paginate the questions by 10. 
        Get the likes and dislikes of the questions.
        Sort the questions by number of likes.
        Add the answers of the question and their likes and dislikes.
        '''
        questions = Question.objects.filter(topics=topic)
        paginator = Paginator(questions, 10)
        page_number = 1
        questions = paginator.get_page(page_number)
        for question in questions:
            likes, dislikes = HomePageQueries.get_votes(question)
            question.likes = likes
            question.dislikes = dislikes

            # add the answers of the question and their likes and dislikes
            answers = Answer.objects.filter(question=question)

            answers_list = []
            
            for answer in answers:
                likes, dislikes = HomePageQueries.get_votes_answers(answer)
                answer.likes = likes
                answer.dislikes = dislikes
                answers_list.append(answer)

            # sort the answers by number of likes
            answers_list.sort(key=lambda x: x.likes, reverse=True)

            # take only the first two answers
            answers_list = answers_list[:2]

            question.answers = answers_list

        questions_list = list(questions)
        questions_list.sort(key=lambda x: x.likes, reverse=True)
        return questions_list
    
    @staticmethod
    def get_all_topics():
        '''
        This method returns all the topics.
        '''
        topics = Topic.objects.all()

        # on each topic add the author.designation
        for topic in topics:
            author = topic.author
            user = CustomUser.objects.get(username=author)
            topic.designation = user.designation
            print(user.designation)

        return topics
    