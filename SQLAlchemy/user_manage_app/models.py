from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """
        Модель пользователя для базы данных.

        Атрибуты:
            id (int): Уникальный идентификатор пользователя.
            name (str): Имя пользователя.
            email (str): Адрес электронной почты пользователя (должен быть уникальным).
            password (str): Зашифрованный пароль пользователя.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """
            Устанавливает зашифрованный пароль для пользователя.
            Args:
                password (str): Пароль, который нужно зашифровать.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
            Проверяет, соответствует ли введенный пароль зашифрованному паролю.
            Args:
                password (str): Пароль, который нужно проверить.
            Returns:
                bool: True, если пароли совпадают, иначе False.
        """
        return check_password_hash(self.password, password)
