# final/views.py
from django.shortcuts import render
from posts.models import Post
from notices.models import Notice

def home(request):
    latest_posts = Post.objects.all().order_by('-created_at')[:5]
    latest_notices = Notice.objects.order_by('-created_at')[:5]  # 최신 5개만
    return render(request, 'home.html', {'latest_posts': latest_posts, 'latest_notices': latest_notices})