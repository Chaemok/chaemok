'''
pjt 06 
F04 - def create_post(request):
F05 - def create_comment(request, post_id):
F13 - index, def 
F15 detail_post
F14 - create_post
F16 edit_post
F17 Delete post
--- edit_comment
F19 delete_comment
'''

# posts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def index(request):
    posts = Post.objects.all().order_by('-created_at')  # 모든 게시글을 가져옵니다. orderby 최신순
    return render(request, 'posts/index.html', {'posts': posts})  # 템플릿에 전달


# F04, F14
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # 게시글 작성자가 현재 로그인한 사용자로 설정
            post = form.save(commit=False)
            post.author = request.user
            post.save()  # 게시글 저장
            return redirect('posts:index')  # 게시글 작성 후 게시글 목록으로 리다이렉트
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


# F05 F18
@login_required
def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)  # 댓글을 작성할 게시글 가져오기
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # 댓글 작성자를 현재 로그인한 사용자로 설정
            comment.post = post  # 댓글이 속할 게시글 설정
            comment.save()  # 댓글 저장
            return redirect('posts:detail_post', post_id=post.id)  # 게시글 상세 페이지로 리다이렉트
    else:
        form = CommentForm()

    return render(request, 'posts/create_comment.html', {'form': form, 'post': post})

# F15
@login_required
def detail_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # 가장 단순/확실한 방식
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'posts/detail_post.html', {
        'post': post,
        'comments': comments,
    })
# F16
@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id) # 수정할 게시글 가져오기

    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("본인 글만 수정할 수 있습니다.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save() # 수정된 데이터 저장
            return redirect('posts:detail_post', post_id=post.id) # 게시글 목록 페이지로 리다이렉트
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/update_post.html', {'form': form, 'post': post})

#F17
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 작성자 본인 또는 관리자만 삭제 가능
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("본인 글만 삭제할 수 있습니다.")

    post.delete()
    return redirect('posts:index')

# # (F18)
# @login_required
# def update_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)  # 수정할 댓글 가져오기

#     if request.user != comment.author and not request.user.is_superuser:
#         return HttpResponseForbidden("본인 댓글만 수정할 수 있습니다.")

#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()  # 수정된 댓글 저장
#             return redirect('posts:detail_post', post_id=comment.post.id)  # 게시글 상세 페이지로 리다이렉트
#     else:
#         form = CommentForm(instance=comment)

#     return render(request, 'posts/update_comment.html', {'form': form, 'comment': comment})


# # F19
# @login_required
# def delete_comment(request, post_id, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)

#     if request.user != comment.author and not request.user.is_superuser:
#         return HttpResponseForbidden('본인 댓글만 삭제할 수 있습니다.')
    
#     comment.delete()
#     return redirect('posts:detail_post', post_id=post_id)

@login_required
def update_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    # 권한 체크
    if request.user != comment.author and not request.user.is_superuser:
        # 권한 없으면 게시글 디테일로 돌려보내거나 403 처리
        return redirect("posts:detail_post", post_id=post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("posts:detail_post", post_id=post.id)
    else:
        form = CommentForm(instance=comment)

    context = {
        "form": form,
        "post": post,
        "comment": comment,
    }
    return render(request, "posts/update_comment.html", context)


@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.user != comment.author and not request.user.is_superuser:
        return redirect("posts:detail_post", post_id=post.id)

    if request.method == "POST":
        comment.delete()
        return redirect("posts:detail_post", post_id=post.id)

    # GET 요청이면 "정말 삭제할까요?" 페이지 보여주는 패턴이라면:
    return render(request, "posts/delete_comment.html", {
        "post": post,
        "comment": comment,
    })
