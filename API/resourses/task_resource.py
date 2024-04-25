from flask_restful import Resource
from models import Task
from flask import make_response, jsonify
import db_session
from API.parser.task_arguments_parser import task_parser
import datetime
db_session.global_init("database.db")
session = db_session.create_session()


class TaskResource(Resource):
    def get(self, task_id):
        task = session.query(Task).get(task_id)
        if task is None:
            return make_response(jsonify({'error': 'Задание не найдено'}), 404)
        return make_response(jsonify(task.to_dict()), 200)

    def put(self, task_id):
        task = session.query(Task).get(task_id)
        if task is None:
            return make_response(jsonify({'error': 'Задание не найдено'}), 404)

        args = task_parser.parse_args()
        task.subject = args['subject'] if args['subject'] else task.subject
        task.number = args['number'] if args['number'] else task.number
        task.description = args['description'] if args['description'] else task.description
        task.condition = args['condition'] if args['condition'] else task.condition
        task.answer = args['answer'] if args['answer'] else task.answer
        task.code_answer = args['code_answer'] if args['code_answer'] else task.code_answer
        task.date = 'Опубликовано' + task.date[:(task.date.index('И') if 'И' in task.date else -1)] + 'Изменено:' + str(
            datetime.datetime.now())
        if args['photo']:
            task.photo_url = args['photo_url']
        if args['answer_photo']:
            task.answer_photo_url = args['answer_photo_url']
        session.commit()
        return make_response(jsonify({'message': 'Задание успешно обновлено', 'task': task.to_dict()}), 200)

    def delete(self, task_id):
        task = session.query(Task).get(task_id)
        if task is None:
            return make_response(jsonify({'error': 'Задание не найдено'}), 404)

        session.delete(task)
        session.commit()
        return make_response(jsonify({'message': 'Задание успешно удалено'}), 200)


class TaskListResource(Resource):
    def get(self):
        tasks = session.query(Task).all()
        return make_response(jsonify({'tasks': [task.to_dict() for task in tasks]}), 200)

    def post(self):
        args = task_parser.parse_args()
        print(args)
        new_task = Task()
        args = task_parser.parse_args()
        new_task.subject = args['subject']
        new_task.number = args['number']
        new_task.description = args['description'] if args['description'] else None
        new_task.condition = args['condition']
        new_task.answer = args['answer']
        new_task.code_answer = args['code_answer'] if args['code_answer'] else None
        new_task.date = str(datetime.datetime.now())
        if args['photo']:
            new_task.photo_url = args['photo_url']
        if args['answer_photo']:
            new_task.answer_photo_url = args['answer_photo_url']
        session.add(new_task)
        session.commit()
        return make_response(jsonify({'message': 'Задание успешно создано', 'task': new_task.to_dict()}), 201)
