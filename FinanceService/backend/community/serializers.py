# backend/community/serializers.py
from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname') # 작성자 닉네임 가져오기
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'post', 'like_users', 'dislike_users')

class PostSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    # [Nested] 해당 게시글의 댓글들을 리스트로 포함
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    dislike_count = serializers.IntegerField(source='dislike_users.count', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'dislike_users')