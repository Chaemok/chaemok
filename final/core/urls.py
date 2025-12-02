from django.urls import path
from . import views

urlpatterns = [
    path('theme-toggle/', views.theme_toggle, name='theme_toggle'),
]
