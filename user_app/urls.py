# from user_app import
from django.urls import path
from user_app.views import *


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('listgame/', ListGamesView.as_view(), name='listgame'),
    path('getboard/<int:game_id>', GetBoardView.as_view(), name='getboard'),
    path('creategame/', CreateGameView.as_view(), name='creategame'),
    path('updateboard/<int:game_id>', UpdateBoardView.as_view(), name='updateboard'),
]
