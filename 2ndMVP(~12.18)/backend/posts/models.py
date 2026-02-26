# posts/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    # 카테고리 (자유, 공지, 질문, FAQ)
    CATEGORY_CHOICES = [
        ('notice', '공지사항'),
        ('free', '자유게시판'),
        ('qna', '1:1문의'),
        ('faq', 'FAQ'),
    ]

    # 작성자 (User 모델 연결)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # 필드 구성
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField(max_length=200)
    content = models.TextField()    
    # 게시글 좋아요
    like_users = models.ManyToManyField(User, related_name='like_posts', blank=True)
    # Q&A 게시판용: 비밀글 여부 (기본 False)
    is_secret = models.BooleanField(default=False)
    
    # 관리자 답변 여부 (Q&A 관리용)
    is_answered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class Comment(models.Model):
    # Post 모델과 1:N 관계
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    like_users = models.ManyToManyField(User, related_name='like_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]