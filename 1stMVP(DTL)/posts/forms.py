'''
pjt 06 
F04 - PostForm 클래스
F05 - CommentForm 클래스
F06 - Clean 검증 추가
'''
# posts/forms.py
from django import forms
from .models import Post, Comment


from django import forms
from .models import Post


# F04
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input', 'placeholder': '제목을 입력하세요', 'autofocus': 'autofocus'
            }),
            'content': forms.Textarea(attrs={
                'class': 'textarea', 'rows': 14, 'placeholder': '내용을 입력하세요'
            }),
        }


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content']  # 게시글 작성 시 필요한 필드

#     # 커스터마이즈한 clean 메서드로 필드 검증 추가 F06
#     def clean_title(self): #F06
#         title = self.cleaned_data.get('title')
#         if not title:
#             raise forms.ValidationError('제목을 입력하세요.')
#         return title

#     def clean_content(self): #F06
#         content = self.cleaned_data.get('content')
#         if not content:
#             raise forms.ValidationError('내용을 입력하세요.')
#         return content


# F05
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # 댓글 작성 시 필요한 필드
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'textarea', 'rows': 14, 'placeholder': '내용을 입력하세요'
            }),
        }

    
    # 댓글 내용 검증 F06
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('댓글 내용을 입력하세요.')
        return content
    
