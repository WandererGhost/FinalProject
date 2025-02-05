from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    """
        Форма для ввода данных пользователя.
        Атрибуты:
            name (StringField): Поле для ввода имени пользователя.
            email (StringField): Поле для ввода адреса электронной почты.
            password (PasswordField): Поле для ввода пароля.
            submit (SubmitField): Кнопка для отправки формы.
    """
    name = StringField('Имя', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Сохранить')
