# posts/urls.py

from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<int:post_pk>/like/', views.like_post, name='like_post'),
    path('<int:post_pk>/comments/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
    path('comments/<int:comment_pk>/like/', views.like_comment, name='like_comment'),
]