'''
This file contains the code for the chat view. The chat view is responsible for handling the user input, making the API request to OpenAI, and displaying the conversation history on the chatbot interface.
'''
from urllib.parse import urlparse
from django.shortcuts import render
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

def chat(request):
    global conversation

    # Check if the user has sent a message
    if request.method == 'POST' and 'user_input' in request.POST:
        user_input = request.POST['user_input'].strip()

        # Add the user input to the conversation history
        conversation.append('User: ' + user_input)

        # Create a prompt with the conversation history for context
        prompt = '\n'.join(conversation) + '\nAI:'

        # Get the response from OpenAI API
        ai_response = ask_openai(user_input)

        # Add the AI response to the conversation history
        conversation.append('AI: ' + ai_response)

    # Pass the conversation history to the template context
    context = {
        'conversation': conversation
    }

    return context

    # redirect to home page with extra context

    # # Get the referring page URL
    # referring_page = request.META.get('HTTP_REFERER')

    # # Parse the referring page URL to extract the base URL and path
    # parsed_url = urlparse(referring_page)
    # base_url = parsed_url.scheme + '://' + parsed_url.netloc
    # referring_path = parsed_url.path

    # # Redirect back to the referring page
    # return render(request, referring_path, context)