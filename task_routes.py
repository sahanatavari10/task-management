from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, db

task_bp = Blueprint('task', __name__)

@task_bp.route('/task', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()
    task = Task(title=data['title'], description=data.get('description'), user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify("Task created", task_id=task.id), 201

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    result = [{'id':t.id, 'title':t.title, 'description':t.description, 'completed':t.completed} for t in tasks]
    return jsonify(result)

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_tasks(task_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify(message="Task not found"), 404
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(message="Task updated"), 200

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify("Task not found"), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify(message="Task deleted"), 200