# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('me/', views.me, name='me'),
    path('password/change/', views.change_password, name='change_password'),
    path('check-username/<str:username>/', views.check_username, name='check_username'),
    path('check-nickname/<str:nickname>/', views.check_nickname, name='check_nickname'),
]   