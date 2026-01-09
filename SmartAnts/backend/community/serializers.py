from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    dislike_count = serializers.IntegerField(source='dislike_users.count', read_only=True)
    # 🐜 [추가] 현재 로그인한 유저가 좋아요/싫어요 눌렀는지 확인
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'dislike_users')

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.like_users.filter(pk=user.pk).exists()
        return False

    def get_is_disliked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.dislike_users.filter(pk=user.pk).exists()
        return False

class PostSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    dislike_count = serializers.IntegerField(source='dislike_users.count', read_only=True)
    # 🐜 [추가] 게시글도 마찬가지로 상태 확인
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'dislike_users')

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.like_users.filter(pk=user.pk).exists()
        return False

    def get_is_disliked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.dislike_users.filter(pk=user.pk).exists()
        return False