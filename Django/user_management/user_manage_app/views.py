from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import UserForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
import logging


logger = logging.getLogger('user_manage_app')


# Создание пользователя
def create_user(request):
    """
    Представление для создания нового пользователя.
    Обрабатывает POST-запросы для сохранения нового пользователя в базе данных.
    При успешном создании выполняет редирект на страницу со списком пользователей.
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f'Пользователь успешно создан.')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_manage_app/user_form.html', {'form': form})


# Получение списка пользователей
def user_list(request):
    """
    Представление для списка пользователей
    """
    users = User.objects.all()
    logger.info(f'Список пользователей успешно получен')
    return render(request, 'user_manage_app/user_list.html', {'users': users})


# Обновление пользователя
def update_user(request, user_id):
    """
    Представление для обновления пользователя.
    Обрабатывает POST-запросы для сохранения новых данных пользователя в базе данных.
    При успешном обновлении выполняет редирект на страницу со списком пользователей.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            logger.info(f'Пользователь успешно обновлён.')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_manage_app/user_form.html', {'form': form})


# Удаление пользователя
def delete_user(request, user_id):
    """
    Представление для удаления пользователя.
    Обрабатывает POST-запросы для сохранения нового пользователя в базе данных.
    При успешном создании выполняет редирект на страницу со списком пользователей.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        logger.info(f'Пользователь успешно удалён.')
        return redirect('user_list')
    return render(request, 'user_manage_app/user_confirm_delete.html', {'user': user})


#  Реализация входа
def user_login(request):
    """
    Представление для входа пользователя.
    Обрабатывает POST-запросы.
    При успешном входе выполняет редирект на страницу со списком пользователей.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f'Пользователь успешно залогинился.')
                return redirect('user_list')  # Перенаправление на список пользователей
    else:
        form = LoginForm()
    return render(request, 'user_manage_app/login.html', {'form': form})


#  Реализация выхода
def user_logout(request):
    """
    Представление для выхода пользователя.
    Обрабатывает POST-запросы
    При успешном создании выполняет редирект на страницу со списком пользователей.
    """
    logout(request)
    logger.info(f'Пользователь вышел.')
    return redirect('user_list')  # Перенаправление на список пользователей
