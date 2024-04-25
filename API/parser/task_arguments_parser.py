from flask_restful import reqparse

task_parser = reqparse.RequestParser()
task_parser.add_argument('subject', type=str, required=True, help='Название предмета')
task_parser.add_argument('number', type=int, required=True, help='Номер задания обязателен')
task_parser.add_argument('description', type=str, help='Описание (необязательный параметр)')
task_parser.add_argument('condition', type=str, required=True, help='Условие обязательно')
task_parser.add_argument('answer', type=str, required=True, help='Ответ обязателен')
task_parser.add_argument('code_answer', type=str, help='Ответ в виде кода (необязательный параметр, будет показан только в разделе информатики)')
task_parser.add_argument('photo_url', type=str, help='Фото (необязательный параметр)')
task_parser.add_argument('answer_photo_url', type=str, help='Фот для ответа (необязательный параметр)')

