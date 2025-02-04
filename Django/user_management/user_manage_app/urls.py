from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),  # Список пользователей
    path('create/', views.create_user, name='create_user'),  # Создание пользователя
    path('update/<int:user_id>/', views.update_user, name='update_user'),  # Обновление пользователя
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),  # Удаление пользователя
    path('login/', views.user_login, name='user_login'),  # Вход
    path('logout/', views.user_logout, name='user_logout'),  # Выход
]
