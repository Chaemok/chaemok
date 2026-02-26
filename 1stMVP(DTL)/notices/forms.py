from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': '제목'}),
            'content': forms.Textarea(attrs={'class': 'textarea', 'rows': 10, 'placeholder': '내용'}),
        }