from flask import request, jsonify, Blueprint
from database import db
from models import User, List, Task
from auth import generate_token, decode_token, token_required
import jwt

bp = Blueprint('main', __name__)

@bp.errorhandler(500)
def internal_server_error(error):
    return jsonify({"message": "An internal error occurred."}), 500

@bp.errorhandler(400)
def bad_request_error(error):
    return jsonify({"message": "Bad request."}), 400

@bp.route('/')
def home():
    return "Hello, this is the home page of the Todo App!"

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already registered!"}), 400
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.password == data.get('password'):
        token = generate_token(user.id)
        return jsonify({"token": token, "message": "Logged in successfully!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@bp.route('/list', methods=['POST'])
@token_required
def create_list(current_user_id):
    data = request.get_json()
    listInst = List(title=data['title'], user_id=current_user_id)
    db.session.add(listInst)
    db.session.commit()
    user_lists = List.query.filter_by(user_id=current_user_id).all()
    lists_data = [task.to_dict(recursive=False) for task in user_lists]
    return jsonify(lists_data)

@bp.route('/task', methods=['POST'])
@token_required
def create_task(current_user_id):
    data = request.get_json()
    task = Task(title=data['title'], content=data['content'], list_id=data['list_id'], parent_id=data.get('parent_id'))
    db.session.add(task)
    db.session.commit()
    user_tasks = Task.query.filter_by(list_id=data['list_id']).all()
    tasks_data = [task.to_dict(recursive=False) for task in user_tasks]
    return jsonify(tasks_data)

@bp.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    return jsonify({"title": task.title, "content": task.content})

@bp.route('/lists', methods=['GET'])
@token_required
def lists(current_user_id):
    user_lists = List.query.filter_by(user_id=current_user_id).all()
    lists_data = [list.to_dict(recursive=False) for list in user_lists]
    return jsonify(lists_data)

@bp.route('/tasks', methods=['GET'])
@token_required
def tasks(current_user_id):
    user_tasks = Task.query.filter_by(user_id=current_user_id).all()
    tasks_data = [task.to_dict(recursive=False) for task in user_tasks]
    return jsonify(tasks_data)

@bp.route('/task/<int:task_id>/<int:list_id>', methods=['PUT'])
@token_required
def update_task(current_user_id, task_id, list_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    if task.list_id != list_id:
        return jsonify({"message": "Access denied!"}), 403
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.content = data.get('content', task.content)
    db.session.commit()
    return jsonify({"message": "Task updated successfully!"})

@bp.route('/task/<int:task_id>/<int:list_id>', methods=['DELETE'])
@token_required
def delete_task(current_user_id, task_id, list_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    if task.list_id != list_id:
        return jsonify({"message": "Access denied!"}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"})

@bp.route('/task/<int:parent_task_id>/subtask', methods=['POST'])
@token_required
def create_subtask(current_user_id, parent_task_id):
    parent_task = Task.query.get(parent_task_id)
    if not parent_task:
        return jsonify({"message": "Parent task not found!"}), 404
    data = request.get_json()
    print(parent_task_id)
    subtask = Task(title=data['title'], content=data['content'], parent_id=parent_task_id)
    db.session.add(subtask)
    db.session.commit()
    return jsonify(subtask.id), 201

@bp.route('/task/<int:task_id>/subtasks', methods=['GET'])
@token_required
def get_subtasks(current_user_id, task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    subtasks = [{"id": subtask.id, "title": subtask.title, "content": subtask.content} for subtask in task.children]
    return jsonify(subtasks)

@bp.route('/task/<int:task_id>/hierarchy', methods=['GET'])
@token_required
def get_task_hierarchy(current_user_id, task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    return jsonify(task.to_dict())

@bp.route('/task/<int:task_id>/move', methods=['PUT'])
@token_required
def move_task(current_user_id, task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    data = request.get_json()

    # Update the parent_id to move the task
    task.list_id = data['new_list_id']
    db.session.commit()

    return jsonify({"message": "Task moved successfully!"})


@bp.route('/task/<int:task_id>/add_label', methods=['PUT'])
@token_required
def add_label_to_task(current_user_id, task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    data = request.get_json()
    label = data.get('label')
    if not label:
        return jsonify({"message": "Label not provided!"}), 400
    task.labels.append(label)
    db.session.commit()
    return jsonify({"message": "Label added successfully!"})
@bp.route('/list/<int:list_id>', methods=['DELETE'])
@token_required
def delete_list(current_user_id, list_id):
    list_to_delete = List.query.get(list_id)
    if not list_to_delete:
        return jsonify({"message": "List not found!"}), 404
    if list_to_delete.user_id != current_user_id:
        return jsonify({"message": "Access denied!"}), 403

    # Delete the list
    db.session.delete(list_to_delete)
    db.session.commit()
    return jsonify({"message": "List deleted successfully!"})