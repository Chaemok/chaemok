from django.db.models import Q
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrAdminReadOnly

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all().order_by('-created_at')
        
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category=category)

        if self.action == 'mine':
            return queryset.filter(user=user)

        if not user.is_authenticated:
            return queryset.filter(is_secret=False)
        if user.is_staff:
            return queryset
        return queryset.filter(Q(is_secret=False) | Q(user=user))
    
    def perform_create(self, serializer):
        category = self.request.data.get('category')
        is_secret = self.request.data.get('is_secret', False)
        if category == 'inquiry': is_secret = True
        serializer.save(user=self.request.user, is_secret=is_secret)

    @action(detail=False, methods=['get'])
    def mine(self, request):
        posts = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    # 🐜 [수정] 좋아요/싫어요 토글 시 양쪽 카운트를 모두 반환
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.like_users.filter(pk=user.pk).exists():
            post.like_users.remove(user)
            liked = False
        else:
            post.like_users.add(user)
            post.dislike_users.remove(user)
            liked = True
        return Response({
            'liked': liked, 
            'like_count': post.like_users.count(),
            'dislike_count': post.dislike_users.count()
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.dislike_users.filter(pk=user.pk).exists():
            post.dislike_users.remove(user)
            disliked = False
        else:
            post.dislike_users.add(user)
            post.like_users.remove(user)
            disliked = True
        return Response({
            'disliked': disliked, 
            'like_count': post.like_users.count(),
            'dislike_count': post.dislike_users.count()
        }, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mine(self, request):
        comments = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    # 🐜 댓글도 동일하게 양쪽 카운트 반환 처리
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if comment.like_users.filter(pk=user.pk).exists():
            comment.like_users.remove(user)
            liked = False
        else:
            comment.like_users.add(user)
            comment.dislike_users.remove(user)
            liked = True
        return Response({
            'liked': liked, 
            'like_count': comment.like_users.count(),
            'dislike_count': comment.dislike_users.count()
        })

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if comment.dislike_users.filter(pk=user.pk).exists():
            comment.dislike_users.remove(user)
            disliked = False
        else:
            comment.dislike_users.add(user)
            comment.like_users.remove(user)
            disliked = True
        return Response({
            'disliked': disliked, 
            'like_count': comment.like_users.count(),
            'dislike_count': comment.dislike_users.count()
        })