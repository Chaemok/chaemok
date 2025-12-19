# backend/community/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 작성자만 수정/삭제 가능하게 하는 권한
    조회(GET, HEAD, OPTIONS)는 누구나 가능
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user