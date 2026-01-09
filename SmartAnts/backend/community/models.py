# backend/community/models.py
from django.db import models
from django.conf import settings

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('inquiry', '1:1 문의'),
        ('free', '자유게시판'),
        ('review', '상품후기'),
        ('qna', 'Q&A'),
        ('tips', '투자꿀팁'),
        ('faq', 'FAQ'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    # 🐜 [수정] 이 필드가 없어서 필터링이 안 됐던 거야!
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='free') 
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_secret = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts', blank=True)
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_posts', blank=True)

    def __str__(self):
        return self.title

# 2. 댓글 모델
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # [추가] 댓글 좋아요 & 싫어요 기능
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments', blank=True)
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_comments', blank=True)

    def __str__(self):
        return f"{self.user.username}의 댓글"