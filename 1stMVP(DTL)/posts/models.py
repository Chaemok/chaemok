'''
11/07 pjt06 
수정
F04 - Post 클래스 만듬
F05 - Comment 클래스 만듬
'''

# posts/models.py

from django.db import models
from django.conf import settings  # settings에서 사용자 모델을 참조
# pjt 06 - F04
class Post(models.Model):
    title = models.CharField(max_length=200)  # 게시글 제목
    content = models.TextField()  # 게시글 내용
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자 모델 참조
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일 (자동으로 현재 시간 저장)

    def __str__(self):
        return self.title  # 게시글의 제목을 문자열로 반환
# pjt 06 - F05
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # 게시글에 대한 댓글
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 댓글 작성자 (User 모델)
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성일 (자동으로 현재 시간 저장)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"  # 댓글 작성자와 게시글 제목을 반환








# settings.AUTH_USER_MODEL   >> 'accounts.CustomUser'
# 왜 models.py에서는 위 처럼 쓰고, 나머지는 get_user_model() 쓰냐??
# get_user_model()은 이미 모델이 다 만들어 져 있는 상태에서 클래스를 직접참조
# 근데...models.py 는 클래스 정의.....아직 얘가 있는지 없는지도 모르는데...get_user_model() 함수를 통해서 접근이 안됨
# 참조 클래스 부분에 '문자열' 형태로 클래스 이름을 지정하면...lazy loading이 일어남...
# lazy loading : 실제로 사용될 때 연산되는거..(미리 연산해놓고 안쓰는거 방지)

'''

from django.db import models
from django.conf import settings
# Create your models here.
'''