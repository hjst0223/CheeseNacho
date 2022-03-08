from django.urls import path
from entmt_info import views

app_name = 'entmt_info'

urlpatterns = [
    path('import/', views.ei_page, name='ei_page'), # API 데이터 다운로드 페이지
    path('import_genre/', views.ei_genre, name='ei_genre'),
    path('import_movie/', views.ei_movie, name='ei_movie'),
    path('import_tv/', views.ei_tv, name='ei_tv'),
    # path('<int:movie_id>/detail/', views.e_detail, name='e_detail'),
    path('detail/', views.e_detail, name='e_detail'),
    # path('detail_jy/', views.e_detail_jy, name='e_detail_jy'),  # 영화 상세내용 업로드
    path('results/', views.e_results, name='e_results'),
    path('submit_comment/<int:media_id>/<media_type>/', views.submit_comment, name='submit_comment'),
    path('delete_comment/<int:comment_id>/<media_type>/', views.delete_comment, name='delete_comment'),
    path('update_comment/<int:comment_id>/<media_type>/', views.update_comment, name='update_comment'),
]
