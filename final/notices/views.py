from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from .models import Notice
from .forms import NoticeForm

def index(request):
    qs = Notice.objects.all()
    paginator = Paginator(qs, 10)  # 페이지당 10개
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'notices/index.html', {'page_obj': page_obj})

def detail_notice(request, notice_id):
    try:
        notice = Notice.objects.get(pk=notice_id)
    except Notice.DoesNotExist:
        raise Http404('공지사항을 찾을 수 없습니다.')
    return render(request, 'notices/detail.html', {'notice': notice})

def _staff_only(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(_staff_only)
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            if request.user.is_authenticated:
                notice.author = request.user
            notice.save()
            return redirect('notices:detail_notice', notice_id=notice.id)
    else:
        form = NoticeForm()
    return render(request, 'notices/form.html', {'form': form, 'mode': 'create'})

@user_passes_test(_staff_only)
def update_notice(request, notice_id):
    try:
        notice = Notice.objects.get(pk=notice_id)
    except Notice.DoesNotExist:
        raise Http404('공지사항을 찾을 수 없습니다.')

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notices:detail_notice', notice_id=notice.id)
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'notices/form.html', {'form': form, 'mode': 'update', 'notice': notice})

@user_passes_test(_staff_only)
def delete_notice(request, notice_id):
    try:
        notice = Notice.objects.get(pk=notice_id)
    except Notice.DoesNotExist:
        raise Http404('공지사항을 찾을 수 없습니다.')

    if request.method == 'POST':
        notice.delete()
        return redirect('notices:index')
    # GET으로 접근하면 간단 확인 화면
    return render(request, 'notices/confirm_delete.html', {'notice': notice})
