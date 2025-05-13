from flask import Blueprint, request, jsonify
from models import db, User

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('email') or '@' not in data.get('email'):
        return jsonify({'error': 'Invalid email format'}), 400
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 201

@user_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})