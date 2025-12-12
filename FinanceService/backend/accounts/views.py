# accounts/views.py

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

# 1. 회원가입 (POST)
@api_view(['POST'])
@permission_classes([AllowAny]) # 누구나 접근 가능
def signup(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. 내 정보 조회, 수정, 탈퇴 (GET, PUT, DELETE)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) # 로그인 필수
def me(request):
    user = request.user

    # 조회
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # 수정
    elif request.method == 'PUT':
        # partial=True: 일부 데이터만 수정 가능
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 탈퇴
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 3. 비밀번호 변경 (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    new_password_confirm = request.data.get("new_password_confirm")

    # 1. 현재 비밀번호 확인
    if not user.check_password(old_password):
        return Response({"error": "현재 비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 2. 새 비밀번호 일치 확인
    if new_password != new_password_confirm:
        return Response({"error": "새 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 3. 변경 및 저장
    user.set_password(new_password)
    user.save()
    return Response({"message": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)

# accounts/views.py 에 추가

@api_view(['GET'])
@permission_classes([AllowAny]) # 로그인 안 해도 확인 가능해야 함
def check_username(request, username):
    # 유저 모델에서 해당 username이 있는지 검색
    if User.objects.filter(username=username).exists():
        return Response({"available": False, "message": "이미 사용 중인 아이디입니다."}, status=status.HTTP_200_OK)
    else:
        return Response({"available": True, "message": "사용 가능한 아이디입니다."}, status=status.HTTP_200_OK)
    
# 닉네임 중복 확인
@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request, nickname):
    if User.objects.filter(nickname=nickname).exists():
        return Response({"available": False, "message": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_200_OK)
    return Response({"available": True, "message": "사용 가능한 닉네임입니다."}, status=status.HTTP_200_OK)