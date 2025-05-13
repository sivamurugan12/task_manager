from flask import Blueprint, request, jsonify
from models import db, Task, TaskDependency

task_bp = Blueprint('tasks', __name__)

def check_circular_dependency(task, target_id):
    if task.id == target_id:
        return True
    for dep in task.dependencies:
        if check_circular_dependency(dep, target_id):
            return True
    return False

@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(title=data['title'], user_id=data['user_id'], project_id=data['project_id'])
    db.session.add(task)
    db.session.commit()

    for dep_id in data.get('dependencies', []):
        dep_task = Task.query.get(dep_id)
        if check_circular_dependency(dep_task, task.id):
            return jsonify({'error': 'Circular dependency detected'}), 400
        link = TaskDependency(task_id=task.id, depends_on_id=dep_id)
        db.session.add(link)

    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title}), 201

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'id': task.id, 'title': task.title, 'status': task.status})

@task_bp.route('/<int:task_id>/status', methods=['PUT'])
def update_status(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    for dep in task.dependencies:
        if dep.status != 'completed':
            return jsonify({'error': 'Dependencies not completed'}), 400

    task.status = request.json.get('status')
    db.session.commit()
    return jsonify({'message': 'Status updated'})

@task_bp.route('/user/<int:user_id>', methods=['GET'])
def list_tasks_by_user(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status} for t in tasks])

@task_bp.route('/status/<status>', methods=['GET'])
def list_tasks_by_status(status):
    tasks = Task.query.filter_by(status=status).all()
    return jsonify([{'id': t.id, 'title': t.title, 'user_id': t.user_id} for t in tasks])