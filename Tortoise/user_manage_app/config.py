TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"  # Путь к базе данных
    },
    "apps": {
        "models": {
            "models": ["models"],  # Имя модуля, где находятся ваши модели
            "default": True,
        }
    }
}
