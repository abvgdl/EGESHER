from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Имя пользователя обязательно')
user_parser.add_argument('email', type=str, required=True, help='Email обязателен')
user_parser.add_argument('password', type=str, required=True, help='Пароль обязателен')
user_parser.add_argument('role', type=str, required=True, help='Роль обязательна')
