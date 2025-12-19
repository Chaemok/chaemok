# backend/posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'post', 'like_users')

class PostListSerializer(serializers.ModelSerializer):
    """목록 조회용: 가벼운 정보"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'category', 'title', 'user_name', 'like_count', 'comment_count', 'created_at', 'is_secret')

class PostDetailSerializer(serializers.ModelSerializer):
    """상세 조회용: 모든 필드 + 댓글 포함"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'like_users')