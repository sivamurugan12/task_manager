from flask import Blueprint, request, jsonify
from models import db, Project, Task

project_bp = Blueprint('projects', __name__)

@project_bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(name=data['name'])
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id, 'name': project.name}), 201

@project_bp.route('/', methods=['GET'])
def list_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in projects])

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify({'id': project.id, 'name': project.name})

@project_bp.route('/<int:project_id>/tasks', methods=['GET'])
def list_tasks_under_project(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status} for t in tasks])