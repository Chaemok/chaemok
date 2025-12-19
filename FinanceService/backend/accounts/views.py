# backend/accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

User = get_user_model()

# 1. 회원 탈퇴 (DELETE)
# dj-rest-auth는 탈퇴 기능을 기본 제공하지 않으므로 이 부분은 유지하는 게 좋아!
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    request.user.delete()
    return Response(
        {"message": "회원 탈퇴가 완료되었습니다."}, 
        status=status.HTTP_204_NO_CONTENT
    )

# 2. 아이디 중복 확인 (UX 향상을 위한 커스텀 API)
@api_view(['GET'])
@permission_classes([AllowAny])
def check_username(request, username):
    exists = User.objects.filter(username=username).exists()
    return Response({
        "available": not exists, 
        "message": "이미 사용 중인 아이디입니다." if exists else "사용 가능한 아이디입니다."
    }, status=status.HTTP_200_OK)

# 3. 닉네임 중복 확인 (회원 커스터마이징 F02 관련)
@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request, nickname):
    exists = User.objects.filter(nickname=nickname).exists()
    return Response({
        "available": not exists, 
        "message": "이미 사용 중인 닉네임입니다." if exists else "사용 가능한 닉네임입니다."
    }, status=status.HTTP_200_OK)