from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    """
    Форма для заполнения пользовательских данных.
    Использует класс Meta для автоматизации используемых полей
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'password']  # Поля, которые будем использовать


class LoginForm(AuthenticationForm):
    """
    Форма для входа пользователей.
    Использует класс Meta для автоматизации используемых полей
    """
    class Meta:
        model = User
        fields = ['email', 'password']
