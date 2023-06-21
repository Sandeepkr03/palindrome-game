# from user_app import 
from django.urls import path
from user_app.views import *



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login')
]