# backend/community/views.py
from django.db.models import Q
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


# ViewSet을 사용하면 CRUD 로직을 한 번에 처리할 수 있어 효율적이야
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # 비로그인 유저는 비밀글이 아닌 것만 볼 수 있게 처리
        if not user.is_authenticated:
            return Post.objects.filter(is_secret=False).order_by('-created_at')
        
        # 관리자는 전체, 일반 유저는 공개글 + 내 비밀글
        if user.is_staff:
            return Post.objects.all().order_by('-created_at')
        
        return Post.objects.filter(
            Q(is_secret=False) | Q(user=user)
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        # 🐜 프론트엔드에서 보낸 카테고리 확인 후 비밀글 강제 적용
        category = self.request.data.get('category')
        is_secret = self.request.data.get('is_secret', False)
        
        if category == 'inquiry':
            is_secret = True
            
        serializer.save(user=self.request.user, is_secret=is_secret)

    # [추가] 좋아요 토글 로직
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if post.like_users.filter(pk=user.pk).exists():
            post.like_users.remove(user)
            liked = False
        else:
            post.like_users.add(user)
            post.dislike_users.remove(user) # 좋아요 누르면 싫어요 취소
            liked = True
        
        return Response({'liked': liked, 'count': post.like_users.count()}, status=status.HTTP_200_OK)

    # [추가] 싫어요 토글 로직
    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if post.dislike_users.filter(pk=user.pk).exists():
            post.dislike_users.remove(user)
            disliked = False
        else:
            post.dislike_users.add(user)
            post.like_users.remove(user) # 싫어요 누르면 좋아요 취소
            disliked = True
            
        return Response({'disliked': disliked, 'count': post.dislike_users.count()}, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if comment.like_users.filter(pk=user.pk).exists():
            comment.like_users.remove(user)
            liked = False
        else:
            comment.like_users.add(user)
            comment.dislike_users.remove(user) # 싫어요 자동 취소
            liked = True
        return Response({'liked': liked, 'count': comment.like_users.count()})

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if comment.dislike_users.filter(pk=user.pk).exists():
            comment.dislike_users.remove(user)
            disliked = False
        else:
            comment.dislike_users.add(user)
            comment.like_users.remove(user) # 좋아요 자동 취소
            disliked = True
        return Response({'disliked': disliked, 'count': comment.dislike_users.count()}) 