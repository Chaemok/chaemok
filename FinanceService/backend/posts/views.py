# backend/posts/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.db.models import Q
# Models & Serializers
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer


# =============================================================================
# 1. 게시글 (Post) 관련 Views
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    """
    [GET]  게시글 목록 조회 (카테고리, 검색, 보안 적용)
    [POST] 게시글 작성
    """
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        
        # 1. 카테고리 필터링
        category = request.query_params.get('category')
        if category:
            posts = posts.filter(category=category)

        # [NEW] 2. 검색 기능 추가 (제목 or 내용)
        search_query = request.query_params.get('search')
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        
        # 3. [보안] 1:1 문의(QnA) 게시판 접근 제어
        # 'qna' 카테고리인 경우: 관리자거나 작성자 본인만 볼 수 있음
        if category == 'qna':
            if not request.user.is_staff:
                if request.user.is_authenticated:
                    posts = posts.filter(user=request.user)
                else:
                    return Response([]) # 비로그인은 빈 리스트

        # (선택 사항) 전체 검색 시에도 비밀글은 본인 것만 보이게 하려면?
        # 카테고리가 지정되지 않은 상태(전체글)에서 검색할 때 비밀글이 노출될 수 있으므로
        # 아래와 같은 안전장치를 추가하면 더 좋습니다.
        if not category and not request.user.is_staff:
             # 비밀글이 아니거나(OR) 내 글인 경우만 필터링
             if request.user.is_authenticated:
                 posts = posts.filter(Q(is_secret=False) | Q(user=request.user))
             else:
                 posts = posts.filter(is_secret=False)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, post_pk):
    """
    [GET]    게시글 상세 조회
    [PUT]    게시글 수정 (작성자 본인만)
    [DELETE] 게시글 삭제 (작성자 본인만)
    """
    post = get_object_or_404(Post, pk=post_pk)

    # --- [GET] 상세 조회 ---
    if request.method == 'GET':
        # [보안] QnA 게시글은 작성자 본인이나 관리자만 상세 내용 확인 가능
        if post.category == 'qna':
            if post.user != request.user and not request.user.is_staff:
                return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    # --- [권한 체크] 수정/삭제는 작성자만 가능 ---
    if post.user != request.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # --- [PUT] 게시글 수정 ---
    if request.method == 'PUT':
        serializer = PostDetailSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # --- [DELETE] 게시글 삭제 ---
    elif request.method == 'DELETE':
        post.delete()
        return Response({'detail': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    

# =============================================================================
# 2. 좋아요 (Like) 기능
# =============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_pk):
    """게시글 좋아요 / 좋아요 취소 (Toggle)"""
    post = get_object_or_404(Post, pk=post_pk)
    
    # 이미 좋아요를 눌렀다면 -> 취소 (remove)
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
        liked = False
    # 안 눌렀다면 -> 추가 (add)
    else:
        post.like_users.add(request.user)
        liked = True
    
    return Response({'liked': liked, 'count': post.like_users.count()})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_pk):
    """댓글 좋아요 / 좋아요 취소 (Toggle)"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
        liked = False
    else:
        comment.like_users.add(request.user)
        liked = True
        
    return Response({'liked': liked, 'count': comment.like_users.count()})


# =============================================================================
# 3. 댓글 (Comment) 관련 Views
# =============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, post_pk):
    """특정 게시글에 댓글 작성"""
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        # 댓글 작성자와 해당 게시글 연결 후 저장
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    """댓글 수정 및 삭제 (작성자 본인만 가능)"""
    comment = get_object_or_404(Comment, pk=comment_pk)

    # 권한 체크
    if comment.user != request.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # --- [PUT] 댓글 수정 ---
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # --- [DELETE] 댓글 삭제 ---
    elif request.method == 'DELETE':
        comment.delete()
        return Response({'detail': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)