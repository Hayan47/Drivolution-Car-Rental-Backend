from django.urls import path
from rest_framework.authtoken import views as token_views
from . import views

urlpatterns = [
    path('login/', token_views.obtain_auth_token, name='api_token_auth'),
]