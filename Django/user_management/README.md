# User Management App

Это приложение для управления пользователями с использованием Django и различных ORM библиотек.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <https://github.com/WandererGhost/FinalProject/tree/main>
   cd user_management
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
3. Настройте базу данных и примените миграции:
   ```bash
   python manage.py migrate

# Запуск
Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

Теперь вы можете получить доступ к приложению по адресу http://127.0.0.1:8000/.

Логирование

Логи приложения записываются в файл logs/app.log. Уровень логирования установлен на INFO.
