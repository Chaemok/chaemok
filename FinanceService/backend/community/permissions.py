# backend/community/permissions.py
from rest_framework import permissions

class IsOwnerOrAdminReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 🐜 조회(GET, HEAD, OPTIONS)는 누구나 가능
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 🐜 수정/삭제는 작성자 본인이나 관리자만 가능
        return obj.user == request.user or request.user.is_staff