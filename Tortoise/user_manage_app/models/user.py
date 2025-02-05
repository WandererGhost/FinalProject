from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)  # Уникальный идентификатор
    name = fields.CharField(max_length=255)  # Имя пользователя
    email = fields.CharField(max_length=255, unique=True)  # Электронная почта
    password = fields.CharField(max_length=255)  # Зашифрованный пароль
