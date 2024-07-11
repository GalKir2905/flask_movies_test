from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, BooleanField, RadioField, URLField, FileField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, URL

from .models import Review


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомни меня")
    submit = SubmitField("Войти")


class RegistretionForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Некоректный Email")])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo('password',
                                                                                      message="Пароли не совпадают")])
    submit = SubmitField("Зарегистрироваться")


class ReviewForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    text = TextAreaField(
        'Текст',
        validators=[DataRequired(message="Поле не должно быть пустым")])
    score = RadioField("Оценка", choices=[1, 2, 3, 4, 5])
    submit = SubmitField('Добавить отзыв')


class AddMovieForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(message="Поле не должно быть пустым"),
                                                Length(max=255, message='Введите заголовок длиной до 255 символов')])
    description = TextAreaField('Текст', validators=[DataRequired(message="Поле не должно быть пустым")])
    image = URLField('URL', validators=[DataRequired(message="Введите URL"), URL(message="Введите валидную ссылку")])
    submit = SubmitField('Добавить')
