from django.urls import path
from entmt_info import views

app_name = 'entmt_info'

urlpatterns = [
    # path('<int:movie_id>/detail/', views.e_detail, name='e_detail'),
    path('detail/', views.e_detail, name='e_detail'),
    path('results/', views.e_results, name='e_results'),
]
