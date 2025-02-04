from django.db import models


class User (models.Model):
    """
    Модель пользователя, включающая в себя имя пользвателя, адрес электронной почты и пароль
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Длина для зашифрованного пароля

    def __str__(self):
        return self.name
