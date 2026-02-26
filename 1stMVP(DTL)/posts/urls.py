'''
11/07 pjt06 urls.py 생성
F04, F05
F13
F14
F15
'''

from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_post, name='create_post'), # 게시글 작성 URL F04 F14
    # 추가적인 URL 패턴들
    path("<int:post_id>/", views.detail_post, name="detail_post"), # 게시글 상세 페이지 F13
    path("<int:post_id>/update/", views.update_post, name="update_post"),  # 게시글 수정 F14
    path("<int:post_id>/delete/", views.delete_post, name="delete_post"),  # 게시글 삭제 F14

    path("<int:post_id>/comments/create/", views.create_comment, name="create_comment"),  # 댓글 작성 URL F05 F15
    path("<int:post_id>/comments/<int:comment_id>/update/", views.update_comment, name="update_comment"),  # 댓글 수정 F15
    path("<int:post_id>/comments/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),]  # 댓글 삭제 F15


