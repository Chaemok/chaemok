'''
pjt06 F04
'''
# posts/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)  # Post 모델을 관리자 페이지에 등록
