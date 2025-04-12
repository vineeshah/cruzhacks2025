from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.find_by_id(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Remove sensitive data
    user.pop('password_hash', None)
    return jsonify(user), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Remove fields that should not be updated directly
    data.pop('password_hash', None)
    data.pop('_id', None)
    data.pop('email', None)  # Consider requiring email verification for changes
    data.pop('created_at', None)
    
    updated_user = User.update(user_id, data)
    updated_user.pop('password_hash', None)
    
    return jsonify(updated_user), 200 