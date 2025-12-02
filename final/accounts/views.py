'''
11/07 pjt06 F03
views.py 수정

F07 login_view F08 logout_view()
F09 signup_view F10 회원정보 수정
F11 비밀번호 변경 F16 프로파일 뷰

# 보완

'''

from django.urls import reverse_lazy #추가
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView # 추가
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url # resolve_url 추가
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, CustomPasswordChangeForm

# -----------------------------
# F07 로그인
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "로그인되었습니다.")
            # posts:index가 실제로 있으면 그쪽으로, 없으면 홈으로
            return redirect(resolve_url("home") if _url_exists("home") else "/")
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



# -----------------------------
# F08 로그아웃
# -----------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "로그아웃되었습니다.")
    return redirect('home')


# -----------------------------
# F09 회원가입  (중복 정의 제거)
# -----------------------------
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            login(request, user)   # 가입 후 자동 로그인 원치 않으면 제거 
            # messages.success(request, "회원가입이 완료되었습니다. 로그인해주세요.")            
            # 과제 요구가 '회원가입 후 로그인 페이지'라면 아래 유지


            return redirect('accounts:login')
        else:
            messages.error(request, "입력 값을 확인해주세요.")
            print("SIGNUP ERRORS:", form.errors.as_json())  # 콘솔에서 원인 보기 나중에 삭제
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})



# -----------------------------
# F10 회원정보 수정
# -----------------------------
@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 수정되었습니다.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "입력 값을 확인해주세요.")
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'accounts/update_profile.html', {
        'form': form,
        "user": user,
    })


# -----------------------------
# F11 계정 삭제 (POST 전용 권장)
# -----------------------------
@login_required # 로그인한 사용자만 계정 삭제 가능
@require_POST 
def delete_account(request):
    username = request.user.username # 현재 로그인한 사용자
    request.user.delete() # 계정 삭제
    messages.warning(request, f"{username} 계정이 삭제되었습니다.") 
    return redirect('accounts:login') # 로그인 페이지로 리다이렉트


# -----------------------------
# F12 비밀번호 변경 (함수형 유지)
# -----------------------------
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # 비번 저장
            update_session_auth_hash(request, user)  # 세션 유지
            messages.success(request, "비밀번호가 변경되었습니다.")
            return redirect('accounts:change_password_done')
        else:
            messages.error(request, "입력 값을 확인해주세요.")
            print("PWD-CHANGE ERRORS:", form.errors.as_json())  # 콘솔 확인용 나중에 삭제
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def change_password_done(request):
    return render(request, 'accounts/change_password_done.html')

# -----------------------------
# F16 프로필 보기
# -----------------------------
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')  # profile.html 템플릿 렌더링

# -----------------------------
# 관리자 보기: 클래스/함수 중 하나만 사용
# → 여기선 클래스형만 유지
# -----------------------------
class AdminView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounts/admin_view.html'
    permission_required = 'auth.change_user'


# -----------------------------
# 내부 유틸: URL 존재 확인 (안전 리다이렉트용)
# -----------------------------
from django.urls import NoReverseMatch, reverse

def _url_exists(name: str) -> bool:
    try:
        reverse(name)
        return True
    except NoReverseMatch:
        return False