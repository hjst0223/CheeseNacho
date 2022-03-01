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
    path('results/', views.e_results, name='e_results'),
]
