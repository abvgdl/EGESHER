from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class User(UserMixin, SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(15), nullable=False)

    publicated_tasks = relationship("Task", back_populates='author')
    comments = relationship('Comment', back_populates='author')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    subject = Column(String(30), nullable=False)
    number = Column(Integer)
    description = Column(String(60))
    author_id = Column(Integer, ForeignKey('users.id'))
    condition = Column(String)
    answer = Column(String)
    code_answer = Column(String)
    date = Column(String)
    photo_url = Column(String)
    answer_photo_url = Column(String)

    author = relationship('User', back_populates='publicated_tasks')
    comments = relationship('Comment', back_populates='task')


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    date = Column(String)

    task = relationship('Task', back_populates='comments')
    author = relationship('User', back_populates='comments')
