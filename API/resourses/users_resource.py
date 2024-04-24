from flask_restful import Resource
from models import User
from flask import make_response, jsonify
import db_session
from API.parser.users_arguments_parser import user_parser

db_session.global_init("database.db")
session = db_session.create_session()


class UsersResource(Resource):
    def get(self, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            return make_response(jsonify({'error': 'Пользователь не найден'}), 404)
        return make_response(jsonify(user.to_dict()), 200)

    def put(self, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            return make_response(jsonify({'error': 'Пользователь не найден'}), 404)

        args = user_parser.parse_args()
        user.username = args['username']
        user.email = args['email']
        user.set_password(args['password'])
        session.commit()
        return make_response(jsonify({'message': 'Пользователь успешно обновлен', 'user': user.to_dict()}), 200)

    def delete(self, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            return make_response(jsonify({'error': 'Пользователь не найден'}), 404)

        session.delete(user)
        session.commit()
        return make_response(jsonify({'message': 'Пользователь успешно удален'}), 200)


class UsersListResource(Resource):
    def get(self):
        users = session.query(User).all()
        print(users)
        return make_response(jsonify({'users': [user.to_dict() for user in users]}), 200)

    def post(self):
        args = user_parser.parse_args()
        print(args)
        new_user = User()
        new_user.id = len(session.query(User).all()) + 1
        new_user.username = args['username']
        new_user.email = args['email']
        new_user.role = args['role']
        new_user.set_password(args['password'])
        session.add(new_user)
        session.commit()
        return make_response(jsonify({'message': 'Пользователь успешно создан', 'user': new_user.to_dict()}), 201)
