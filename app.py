from flask_restful import Api
from API.resourses import users_resource
import os
from flask import Flask
import db_session
from flask_login import LoginManager, login_required, logout_user
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

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
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, '/static/images/uploads')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
