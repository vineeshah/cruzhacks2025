from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from flask_bcrypt import generate_password_hash, check_password_hash

# Define blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        password_hash = generate_password_hash(data['password']).decode('utf-8')
        user = User.create(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            health_goals=data.get('health_goals', []),
            dietary_restrictions=data.get('dietary_restrictions', []),
            budget_preference=data.get('budget_preference', 'medium')
        )
        return jsonify(user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.find_by_email(data['email'])
        if user and check_password_hash(user['password_hash'], data['password']):
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify({"access_token": access_token}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
