'''
This file contains all the views that are used in the home page.
'''

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.common.queries import HomePageQueries
from posts.forms import FileUploadForm
from posts.models import UploadedFile
from django.shortcuts import render, redirect
from pdfminer.pdfparser import PDFSyntaxError
import requests
import os
# The API key you obtained from OpenAI
API_KEY = os.getenv("OPEN_AI_API_KEY") 

# Initialize conversation history
conversation = []

# Function to make the API request and return the response
def ask_openai(prompt):
    '''
    Function to make the API request and return the response
    '''
    global API_KEY

    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': prompt}
    ]

    data = {
        'model': 'gpt-3.5-turbo',  # Replace with the model you intend to use
        'messages': messages
    }

    api_url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + API_KEY
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        responseData = response.json()
        return responseData['choices'][0]['message']['content']
    else:
        return "I'm sorry, I encountered an error: " + response.text

conversation = []

class HomePageView(LoginRequiredMixin, TemplateView):
    '''
    This class handles the home page view.
    '''
    template_name = "posts/templates/home.html"

    def post(self, request, *args, **kwargs):
        user_input = request.POST.get('user_input', '').strip()
        if user_input:
            # Add the user input to the conversation history
            conversation.append('User: ' + user_input)

            # Create a prompt with the conversation history for context
            prompt = '\n'.join(conversation) + '\nAI:'

            # Get the response from OpenAI API
            ai_response = ask_openai(user_input)

            # Add the AI response to the conversation history
            conversation.append('AI: ' + ai_response)

        # Pass the conversation history to the template context
        context = self.get_context_data()
        context['conversation'] = conversation
        return render(request, 'posts/templates/home.html', context)

    def get_context_data(self, **kwargs):
        '''
        This method handles the get request.
        '''
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context["topics"] = user.followed_topics.all()

        # Get followed questions along with likes and dislikes
        context["followed_questions"] = HomePageQueries.get_user_questions(user)
        context["promoted_questions"] = HomePageQueries.get_all_popular_questions()

        # Pass the conversation history to the template context
        context['conversation'] = conversation

        return context


class SearchView(LoginRequiredMixin, TemplateView):
    '''
    This class handles the search view.
    '''
    template_name = "posts/templates/home.html"

    def post(self, request, *args, **kwargs):
        '''
        This method handles the post request.
        '''
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context["topics"] = user.followed_topics.all()

        # if search is empty string, return all followed questions
        if len(request.POST.get('search')) == 0:
            context["followed_questions"] = HomePageQueries.get_user_questions(user)
            return self.render_to_response(context)

        # Get searched questions along with likes and dislikes
        context["searched_questions"], context["searched_topics"] = HomePageQueries.get_searched_questions(request.POST.get('search'))
        context["search_str"] = request.POST.get('search')

        return self.render_to_response(context)


def upload_and_show_files(request):
    # if request.method == 'POST':
    #     form = FileUploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('upload_and_show_files')
    # else:
    #     form = FileUploadForm()
    
    # files = UploadedFile.objects.all()  # Assuming you have a model UploadedFile with 'file' field
    # for file in files:
    #     try:
    #         file.file.open(mode='rb')
    #         content = file.file.read()
    #         if not content.startswith(b'%PDF'):  # Check if the file starts with '%PDF', indicating a valid PDF
    #             file.is_valid_pdf = False
    #         else:
    #             file.is_valid_pdf = True
    #     except PDFSyntaxError:
    #         file.is_valid_pdf = False
    #     finally:
    #         file.file.close()
    
    # return render(request, 'posts/templates/file.html', {'form': form, 'files': files})
    return render(request, 'posts/templates/main_page.html')


def SalesForaceView(request):
        # Render the template with the content
        return render(request, 'posts/templates/salespage.html')


def home(request):
    return render(request, 'posts/templates/main_page.html')

def diagrams(request):
    return render(request, 'posts/templates/diagrams.html')

def about(request):
    return render(request, 'posts/templates/aboutus.html')