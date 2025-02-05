from flask import Flask, render_template, redirect, url_for, request
from models import db, User
from forms import UserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()  # Создает таблицы в базе данных


@app.route('/')
def index():
    """
    Главная страница приложения, отображающая список пользователей.
    Возвращает:
        str: HTML-шаблон с отображением списка пользователей.
    """
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    """
        Страница для добавления нового пользователя.
        Если форма отправлена и валидна, создается новый пользователь и
        происходит перенаправление на главную страницу. В противном случае
        отображается форма для добавления пользователя.
        Возвращает:
            str: HTML-шаблон с формой для добавления пользователя.
    """
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user_form.html', form=form)


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """
        Страница для редактирования существующего пользователя.
        Если форма отправлена и валидна, обновляются данные пользователя.
        В противном случае отображается форма с текущими данными пользователя.
        Args:
            user_id (int): Уникальный идентификатор пользователя.
        Возвращает:
            str: HTML-шаблон с формой для редактирования пользователя.
    """
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user_form.html', form=form, user=user)


@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """
        Удаление пользователя по уникальному идентификатору.
        Удаляет пользователя из базы данных и перенаправляет на главную страницу.
        Args:
            user_id (int): Уникальный идентификатор пользователя.
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
