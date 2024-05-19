'''
Views for the Topic model.
'''

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from posts.models import Topic, Question
from posts.common.queries import TopicPageQueries
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.forms import AddTopicForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

class AddTopicView(LoginRequiredMixin, CreateView):
    '''
    View for adding a new topic
    '''
    form_class = AddTopicForm
    template_name = 'posts/templates/add_topic.html'
    success_url = reverse_lazy('add_topic')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Handle followed_by
        self.object.followed_by.add(self.request.user)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = TopicPageQueries.get_all_topics()

        return context
    


class TopicPageView(ListView):
    '''
    View for displaying the topic page
    '''
    model = Question
    template_name = 'posts/templates/topic.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        context['topic'] = topic
        all_questions = TopicPageQueries.get_topic_questions(topic)

        # Pagination
        paginator = Paginator(all_questions, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            questions = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            questions = paginator.page(paginator.num_pages)

        context['all_questions'] = questions

        return context

class TopicFollowView(LoginRequiredMixin, ListView):
    '''
    View for following a topic
    '''
    model = Topic
    template_name = 'posts/templates/topic.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        context['topic'] = topic
        all_questions = TopicPageQueries.get_topic_questions(topic)

        # Pagination
        paginator = Paginator(all_questions, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            questions = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            questions = paginator.page(paginator.num_pages)

        context['all_questions'] = questions

        return context

    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        topic.followed_by.add(self.request.user)
        return TopicPageQueries.get_topic_questions(topic)

class TopicUnfollowView(LoginRequiredMixin, ListView):
    '''
    View for unfollowing a topic
    '''
    model = Topic
    template_name = 'posts/templates/topic.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        context['topic'] = topic
        all_questions = TopicPageQueries.get_topic_questions(topic)

        # Pagination
        paginator = Paginator(all_questions, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            questions = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            questions = paginator.page(paginator.num_pages)
        context['all_questions'] = questions
        return context


    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        topic.followed_by.remove(self.request.user)
        return TopicPageQueries.get_topic_questions(topic)


