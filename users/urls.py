from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # django 자체 로그인/로그아웃 기능(views.py X)
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.favorite, name='favorite'),
    # path('changePassword/', views.change_password, name='change_password'),
    path('update/', views.update, name='update'),
    path('genre/', views.genre, name='genre'),
    path('genre/edit/', views.edit_genre, name='edit_genre'),
    path('changeImage/', views.change_image, name='change_image'),
    path('mypage/ratings/', views.ratings, name='ratings'),
    path('mypage/profile/', views.profile, name='profile'),
    path('mypage/preference/', views.preference, name='preference'),
    path('mypage/changePassword/', views.change_password, name='change_password'),
]
