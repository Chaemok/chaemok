# backend/community/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, CommentViewSet

router = SimpleRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]