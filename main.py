import flask_login
from requests import get, put, post, delete
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, logout_user
from flask_login import login_user
from flask_restful import Api
from API.resourses import users_resource
import os

from forms import LoginForm, RegistrationForm
from models import User
import db_session

app = Flask(__name__)

api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("database.db")
db_sess = db_session.create_session()


@app.route('/')
@app.route('/index')
def index():
    title = "EGESHER"
    return render_template('base.html', title=title)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
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
            'password': form.password.data
        }
        print(post('http://localhost:5000/api/v2/users', json=json))
        user = db_sess.query(User).filter(User.email == json['email']).first()
        login_user(user, remember=True)
        return redirect("/")
    return render_template('registration.html', form=form)


@app.route('/russian')
def russian():
    return 1


@app.route('/math')
def math():
    return 1


@app.route('/physic')
def physic():
    return


@app.route('/informatics')
def informatics():
    return


if __name__ == '__main__':
    app.run(debug=True)
