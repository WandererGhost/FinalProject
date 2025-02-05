from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields, Model
from pydantic import BaseModel
from typing import List
from tortoise.exceptions import DoesNotExist
import jwt
import datetime
from fastapi.responses import JSONResponse
from fastapi import Request
from config import TORTOISE_ORM

app = FastAPI()

# Регистрация Tortoise ORM
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # Автоматически генерировать схемы
    add_exception_handlers=True,
)


# Определение модели данных
class User(Model):
    id = fields.IntField(pk=True)  # Уникальный идентификатор
    name = fields.CharField(max_length=255)  # Имя пользователя
    email = fields.CharField(max_length=255, unique=True)  # Электронная почта
    password = fields.CharField(max_length=255)  # Зашифрованный пароль


# Pydantic модели для валидации данных
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


# OAuth2 настройки
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"  # Замените на ваш секретный ключ
ALGORITHM = "HS256"


# Функция для создания токена
def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)  # Токен будет действителен 15 минут
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функция для аутентификации пользователя
async def authenticate_user(email: str, password: str):
    user = await User.get_or_none(email=email)
    if user is None or user.password != password:  # Здесь можно добавить проверку на хэшированный пароль
        return False
    return user


# Эндпоинт для получения токена
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Эндпоинт для создания нового пользователя
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    user_obj = await User.create(**user.dict())
    return user_obj


# Эндпоинт для получения списка всех пользователей
@app.get("/users/", response_model=List[UserResponse])
async def get_users():
    try:
        users = await User.all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Эндпоинт для обновления информации о пользователе
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    try:
        user_obj = await User.get(id=user_id)
        user_obj.name = user.name
        user_obj.email = user.email
        user_obj.password = user.password  # Здесь можно добавить шифрование пароля
        await user_obj.save()
        return user_obj
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Эндпоинт для удаления пользователя
@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    try:
        user_obj = await User.get(id=user_id)
        await user_obj.delete()
        return {"message": "User deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Обработчик ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )


# Эндпоинт для проверки работы приложения
@app.get("/")
async def root():
    return {"message": "Hello, World!"}
