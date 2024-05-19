'''
Views for the accounts app
'''
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseBadRequest

from .models import Poll, Vote
from .common import ProfileQueries
from .forms import CustomUserCreationForm, PollForm

class SignUpView(CreateView):
    '''
    View for signing up a new user
    '''
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
   
class ProfileView(LoginRequiredMixin, TemplateView):
    '''
    View for displaying the profile of the user
    '''
    template_name = "profile.html"
    redirect_field_name = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        data, likes, dislikes = ProfileQueries.all_questions(user.id)
        if data is not None and likes is not None and dislikes is not None:
            context["questions"] = data
            context['qlikes'] = likes
            context['qdislikes'] = dislikes
        context["answers"] = ProfileQueries.all_answers(user.id)
        context["topics"] = ProfileQueries.all_topics(user.id)
        context["votes"] = ProfileQueries.all_votes(user.id)
        return context


class CustomLoginView(LoginView):
    '''
    View for logging in the user
    '''
    template_name = "registration/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("profile")

    # if user is authenticated, then redirect to profile page
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("profile")
        return super().get(request, *args, **kwargs)

class UserProfileUpdateView(LoginRequiredMixin, TemplateView):
    '''
    View for updating the user profile
    '''
    template_name = "registration/update_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.first_name = request.POST.get('first_name')
        user.email = request.POST.get('email')
        user.age = request.POST.get('age')
        user.profilePicture = request.FILES.get('profilePicture')
        user.gender = request.POST.get("gender")

        # if age is less than 0, then return form with error
        try:
            if int(user.age) <= 0:
                print("Age should be a positive number")
                return render(request, "registration/update_profile.html",context={"error": "Age should be a positive number"})
        except ValueError:
            return render(request, "registration/update_profile.html", context= {"error": "Age should be a positive number"})
        user.save()
        return redirect("profile")



def create_poll(request):
    '''
    View for creating a poll
    '''
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            options = form.cleaned_data['options'].split(',')
            poll = Poll.objects.create(question=question)
            for option in options:
                poll.options.create(option_text=option.strip())
            return redirect('profile')
    else:
        return redirect('profile')

# views.py

class PollListView(ListView):
    '''
    View for displaying the list of polls
    '''
    model = Poll
    template_name = 'poll_list.html'
    context_object_name = 'polls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if current user has voted on a poll, then poll.done = True, else poll.done = False
        context['polls'] = Poll.objects.all()
        for poll in context['polls']:
            poll.done = False
            if self.request.user.is_authenticated:
                for vote in poll.votes.all():
                    if vote.user == self.request.user:
                        poll.done = True
                        break

        # list of all the options done by the user
        context['user_options'] = [vote.option_id for vote in Vote.objects.filter(user=self.request.user)]


        return context


class VoteView(LoginRequiredMixin, View):
    '''
    View for voting on a poll
    '''
    def post(self, request, poll_id):
        '''
        Post method for voting on a poll
        '''
        option_id = request.POST.get('option_id')
        if option_id:
            # Create a vote record
            Vote.objects.create(poll_id=poll_id, user=request.user, option_id=option_id)
            return redirect('poll_list')
        else:
            return HttpResponseBadRequest("Invalid option ID")

