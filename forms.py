from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms.fields import EmailField, PasswordField, BooleanField, SubmitField, StringField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import photos


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class AddTaskForm(FlaskForm):
    subject = SelectField('Предмет', choices=[("Русский язык", "Русский язык"),
                                              ("Математика", "Математика"),
                                              ("Физика", "Физика"),
                                              ("Информатика", "Информатика")], validators=[DataRequired()])
    number = StringField('Номер задания', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[])
    condition = TextAreaField('Условие', validators=[DataRequired()])
    image = FileField('Изображение для задачи', validators=[FileAllowed(['jpg', 'png'], 'Image only!')])
    answer = StringField('Правильный ответ', validators=[])
    answer_image = FileField('Изображение для ответа',validators=[FileAllowed(['jpg', 'png'], 'Image only!')])
    code_answer = TextAreaField('Код', validators=[])
    submit = SubmitField('Подтвердить')


class SelectTaskForm(FlaskForm):
    task_number = SelectField('Задание №')
    submit = SubmitField('Подтвердить')
