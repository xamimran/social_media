# posts/urls.py
from django.urls import path
from .views import (HomePageView, 
                    LikeQuestionView,
                    DislikeQuestionView,
                    AnswerQuestionView,
                    SearchView,
                    LikeAnswerView,
                    DislikeAnswerView,
                    AddTopicView,
                    TopicPageView,
                    QuestoinView,
                    AboutView,
                    AddQuestionView,
                    AddQuestionFormView,
                    TopicFollowView,
                    TopicUnfollowView,
                    upload_and_show_files,
                    SalesForaceView,
                    diagrams,
                    home,
                    about,
                    chat
                    )

urlpatterns = [
    # path('', HomePageView.as_view(), name='main_page'),
    path('about/<str:target_username>', AboutView.as_view(), name='about'),
    path('aboutus', about, name='aboutus'),

    path('salesforce', SalesForaceView, name='salesforce'),
    path('diagrams/', diagrams, name='diagrams'),


    path('home', HomePageView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),

    path('like/<int:question_id>/', LikeQuestionView.as_view(), name='like_question'),
    path('dislike/<int:question_id>/', DislikeQuestionView.as_view(), name='dislike_question'),
    path('question/<int:question_id>/', QuestoinView.as_view(), name='question_page'),
    path('add_question_form/', AddQuestionFormView.as_view(), name='add_question_form'),
    path('add_question/', AddQuestionView.as_view(), name='add_question'),

    path('answer/<int:question_id>/', AnswerQuestionView.as_view(), name='answer_question'),
    path('like_answer/<int:answer_id>/', LikeAnswerView.as_view(), name='like_answer'),
    path('dislike_answer/<int:answer_id>/', DislikeAnswerView.as_view(), name='dislike_answer'),

    path('add_topic/', AddTopicView.as_view(), name='add_topic'),
    path('topic/<int:topic_id>/', TopicPageView.as_view(), name='topic_page'),
    path('topic/<int:topic_id>/follow/', TopicFollowView.as_view(), name='topic_follow'),
    path('topic/<int:topic_id>/unfollow/', TopicUnfollowView.as_view(), name='topic_unfollow'),

    path('upload-and-show-files/', upload_and_show_files, name='upload_and_show_files'),
 
    path('chat/', chat, name='chat'),

    path('', home, name='main_page'),
]
