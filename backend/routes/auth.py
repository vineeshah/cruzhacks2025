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
        user = User.create(
            email=data['email'],
            password=data['password'],  # Pass the raw password, let User.create handle hashing
            name=data.get('name')
        )
        if user:
            return jsonify({
                "message": "Registration successful! Welcome to Healthify.",
                "user": user
            }), 201
        else:
            return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("\n=== LOGIN ATTEMPT ===")
        print(f"Email: {data.get('email')}")
        
        if not data or 'email' not in data or 'password' not in data:
            print("Missing email or password")
            return jsonify({"error": "Email and password are required"}), 400
            
        user = User.find_by_email(data['email'])
        print(f"User found: {user is not None}")
        
        if not user:
            print("User not found")
            return jsonify({"error": "Invalid email or password"}), 401
            
        print(f"Password verification: {User.verify_password(user, data['password'])}")
        
        if not User.verify_password(user, data['password']):
            print("Invalid password")
            return jsonify({"error": "Invalid email or password"}), 401
            
        # Create access token
        access_token = create_access_token(identity=str(user['id']))
        print("Login successful")
        print("===================\n")
        
        return jsonify({
            "message": "Login successful! Welcome back to Healthify.",
            "access_token": access_token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "name": user.get('name'),
                "health_goals": user.get('health_goals', []),
                "dietary_restrictions": user.get('dietary_restrictions', [])
            }
        }), 200
    except Exception as e:
        print(f"\nLogin error: {str(e)}")
        return jsonify({"error": str(e)}), 400
