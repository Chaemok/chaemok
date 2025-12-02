from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
    path('', views.index, name='index'),                    # 공개 목록
    path('<int:notice_id>/', views.detail_notice, name='detail_notice'),  # 공개 상세
    path('create/', views.create_notice, name='create_notice'),           # staff 전용
    path('<int:notice_id>/update/', views.update_notice, name='update_notice'), # staff 전용
    path('<int:notice_id>/delete/', views.delete_notice, name='delete_notice'), # staff 전용
]