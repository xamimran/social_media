'''
This file is used to define the URL patterns for the accounts app.
'''

from django.urls import path
from .views import SignUpView, ProfileView, CustomLoginView, UserProfileUpdateView, PollListView, create_poll, VoteView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("update_profile/", UserProfileUpdateView.as_view(), name="update_profile"),
    path('polls/', PollListView.as_view(), name='poll_list'),
    path('create_poll/', create_poll, name='create_poll'),
    path('polls/<int:poll_id>/vote/', VoteView.as_view(), name='vote'),
]
