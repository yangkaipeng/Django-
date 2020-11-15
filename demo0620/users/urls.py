from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('register/', views.regitser, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/<int:pk>/update/', views.profile_update, name='profile_update'),
    path('profile/<int:pk>/pwdchange/', views.pwd_change, name='pwd_change'),
]