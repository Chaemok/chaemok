'''
11/07 pjt 06 
F03
forms.py 생성
F07 로그인
F09 회원가입
F10 회원정보 수정
F12 비밀번호 변경

11/08 보완
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model

# CustomUserCreationForm - 회원가입 폼 커스터마이징 # F09 회원가입
class CustomUserCreationForm(UserCreationForm):

    nickname = forms.CharField(
        max_length=50,
        required=True,               # 회원가입에서는 반드시 입력해야 함
        label="닉네임",
    )

    # 추가 필드
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()  # 모델을 CustomUser로 설정
        fields = ['first_name',
                    'last_name',
                    'username',
                    'nickname',
                    'phone_number',
                    'email',
                    'birthdate',
                    'profile_image'
        ]  # 폼에 포함할 필드 설정
    
    # 보완 추가
    def save(self, commit=True):
        user = super().save(commit=False)
        # UserCreationForm는 username/password만 기본 처리 → 커스텀 필드 수동 설정
        user.email = self.cleaned_data.get('email')
        user.birthdate = self.cleaned_data.get('birthdate')   # 모델에 필드가 실제로 있어야 함
        # profile_image는 FileField/ImageField → instance에 바로 할당
        profile_img = self.cleaned_data.get('profile_image')
        if profile_img:
            user.profile_image = profile_img
        if commit:
            user.save()
        return user

# CustomAuthenticationForm - 로그인 폼 커스터마이징 F07 로그인
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = get_user_model()  # 로그인 폼도 CustomUser 모델을 사용
        fields = ['username', 'password']

# F10 회원정보 수정
class CustomUserChangeForm(UserChangeForm):
    # 추가 필드 (프로필 이미지 등)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()  # 현재 설정된 사용자 모델 사용
        fields = [
            'first_name',
            'last_name',
            'nickname',
            'phone_number',
            'email',
            'birthdate',
            'profile_image',
        ]  # 수정할 필드들


class CustomPasswordChangeForm(PasswordChangeForm):
    # 추가 필드를 커스터마이즈하고 싶다면 여기에 추가 가능
    pass

'''
CustomUserCreationForm: 사용자 회원가입 폼을 정의하는 클래스입니다.
여기서 birthdate와 profile_image를 추가했습니다.
required=False로 설정하여 선택 필드로 만들었습니다.

CustomAuthenticationForm: 기본 AuthenticationForm을 상속받아
 사용자 로그인 폼을 커스터마이징한 클래스입니다.

'''