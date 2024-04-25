import flask
import flask_login
from requests import get, put, post, delete
from flask import render_template, redirect
from flask_login import login_required, logout_user
from flask_login import login_user
import datetime

from forms import LoginForm, RegistrationForm, AddTaskForm, SelectTaskForm, WriteCommentForm
from models import User, Task, Comment
from app import app, db_sess, login_manager, photos


@app.route('/')
@app.route('/index')
def index():
    title = "EGESHER"
    return render_template('base.html', title=title)


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        json = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data,
            'role': 'admin'
        }
        print(post('http://localhost:5000/api/v2/users', json=json))
        user = db_sess.query(User).filter(User.email == json['email']).first()
        login_user(user, remember=True)
        return redirect("/")
    return render_template('registration.html', form=form)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        task = Task()
        if db_sess.query(Task).first():
            task.id = db_sess.query(Task).order_by(Task.id.desc()).first().id + 1
        else:
            task.id = 1
        task.subject = form.subject.data
        task.number = form.number.data
        task.description = form.description.data
        task.author_id = flask_login.current_user.id
        task.condition = form.condition.data
        task.answer = form.answer.data
        task.code_answer = form.code_answer.data
        task.date = str(datetime.datetime.now())
        if form.image.data:
            filename = photos.save(form.image.data)
            task.photo_url = photos.url(filename)
        if form.answer_image.data:
            filename = photos.save(form.answer_image.data)
            task.answer_photo_url = photos.url(filename)
        db_sess.add(task)
        db_sess.commit()
        return redirect('/')
    return render_template('add_task.html', form=form)


@app.route('/delete_task/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    print(delete(f'http://localhost:5000/api/v2/tasks/{task_id}'))
    return redirect('/')


@app.route('/russian', methods=['GET', 'POST'])
def russian():
    return redirect(f'/russian/1')


@app.route('/russian/<int:task_number>', methods=['GET', 'POST'])
def russian_task(task_number):
    tasks_count = [str(i) for i in range(1, 28)]
    form = SelectTaskForm()
    comment_form = WriteCommentForm()
    comment = Comment()
    print(comment_form.validate_on_submit(), comment_form.errors)
    if comment_form.validate_on_submit():
        comment.text = comment_form.text.data
        comment.author_id = flask_login.current_user.id
        comment.task_id = flask.request.form["task_id"]
        comment.date = str(datetime.datetime.now())
        print(comment_form.text.data, flask.request.form["task_id"], comment)
        db_sess.add(comment)
        db_sess.commit()
    form.task_number.default = (str(task_number), str(task_number))
    tasks = db_sess.query(Task).filter(Task.number == str(task_number)).filter(Task.subject == "Русский язык").all()
    form.task_number.choices = [(str(i), str(i)) for i in range(1, 28)]
    return render_template('tasks_template.html', form=form, tasks=tasks, tasks_count=tasks_count, subject='russian',
                           comment_form=comment_form)


@app.route('/math')
def math():
    return redirect(f'/math/1')


@app.route('/math/<int:task_number>', methods=['GET', 'POST'])
def math_task(task_number):
    tasks_count = [str(i) for i in range(1, 20)]
    form = SelectTaskForm()
    comment_form = WriteCommentForm()
    comment = Comment()
    print(comment_form.validate_on_submit())
    if comment_form.validate_on_submit():
        comment.text = comment_form.text.data
        comment.author_id = flask_login.current_user.id
        comment.task_id = flask.request.form["task_id"]
        comment.date = str(datetime.datetime.now())
        print(comment_form.text.data, flask.request.form["task_id"], comment)
        db_sess.add(comment)
        db_sess.commit()
    form.task_number.default = (str(task_number), str(task_number))
    tasks = db_sess.query(Task).filter(Task.number == str(task_number)).filter(Task.subject == "Математика").all()
    form.task_number.choices = [(str(i), str(i)) for i in range(1, 20)]
    return render_template('tasks_template.html', form=form, tasks=tasks, tasks_count=tasks_count, subject='math',
                           comment_form=comment_form)


@app.route('/physic')
def physic():
    return redirect(f'/physic/1')


@app.route('/physic/<int:task_number>', methods=['GET', 'POST'])
def physic_task(task_number):
    tasks_count = [str(i) for i in range(1, 27)]
    form = SelectTaskForm()
    comment_form = WriteCommentForm()
    comment = Comment()
    print(comment_form.validate_on_submit())
    if comment_form.validate_on_submit():
        comment.text = comment_form.text.data
        comment.author_id = flask_login.current_user.id
        comment.task_id = flask.request.form["task_id"]
        comment.date = str(datetime.datetime.now())
        print(comment_form.text.data, flask.request.form["task_id"], comment)
        db_sess.add(comment)
        db_sess.commit()
    form.task_number.default = (str(task_number), str(task_number))
    tasks = db_sess.query(Task).filter(Task.number == str(task_number)).filter(Task.subject == "Физика").all()
    form.task_number.choices = [(str(i), str(i)) for i in range(1, 27)]
    return render_template('tasks_template.html', form=form, tasks=tasks, tasks_count=tasks_count, subject='physic',
                           comment_form=comment_form)


@app.route('/informatics')
def informatics():
    return redirect(f'/informatics/1')


@app.route('/informatics/<int:task_number>', methods=['GET', 'POST'])
def informatics_task(task_number):
    tasks_count = [str(i) for i in range(1, 27)]
    form = SelectTaskForm()
    comment_form = WriteCommentForm()
    comment = Comment()
    print(comment_form.validate_on_submit())
    if comment_form.validate_on_submit():
        comment.text = comment_form.text.data
        comment.author_id = flask_login.current_user.id
        comment.task_id = flask.request.form["task_id"]
        comment.date = str(datetime.datetime.now())
        print(comment_form.text.data, flask.request.form["task_id"], comment)
        db_sess.add(comment)
        db_sess.commit()
    form.task_number.default = (str(task_number), str(task_number))
    tasks = db_sess.query(Task).filter(Task.number == str(task_number)).filter(Task.subject == "Информатика").all()
    form.task_number.choices = [(str(i), str(i)) for i in range(1, 27)]
    return render_template('informatics_tasks_template.html', form=form, tasks=tasks, tasks_count=tasks_count,
                           subject='informatics', comment_form=comment_form)


if __name__ == '__main__':
    app.jinja_env.globals.update(delete_task=delete_task)
    app.run(debug=True)
