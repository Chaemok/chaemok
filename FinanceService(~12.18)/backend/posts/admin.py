from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'user', 'like_count', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    inlines = [CommentInline]

    def like_count(self, obj):
        return obj.like_users.count()
    like_count.short_description = '좋아요 수'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'content', 'like_count', 'created_at')
    
    def like_count(self, obj):
        return obj.like_users.count()
    like_count.short_description = '좋아요 수'