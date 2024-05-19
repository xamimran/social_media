'''
This class handles the about view of the target username passed in the url.
'''
from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from accounts.common import ProfileQueries

class AboutView(LoginRequiredMixin, TemplateView):
    '''
    This class handles the about view.
    '''
    template_name = "posts/templates/about.html"

    def get_context_data(self, **kwargs):
        '''
        This method handles the get request.
        '''
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        user = get_object_or_404(CustomUser, username=self.kwargs['target_username'])
        context["target_user"] = user
        context["questions"], context['qlikes'], context['qdislikes'] = ProfileQueries.all_questions(user.id)
        context["answers"] = ProfileQueries.all_answers(user.id)
        context["topics"] = ProfileQueries.all_topics(user.id)
        context["votes"] = ProfileQueries.all_votes(user.id)
        return context
