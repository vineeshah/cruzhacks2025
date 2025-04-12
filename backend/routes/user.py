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

@user_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    print("\n" + "="*50)
    print("PREFERENCES UPDATE ROUTE HIT")
    print("="*50 + "\n")
    
    try:
        user_id = get_jwt_identity()
        print(f"User ID from token: {user_id}")
        
        if not request.is_json:
            print("ERROR: Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        print(f"Raw request data: {data}")
        print(f"Data type: {type(data)}")
        
        # Validate the data structure
        if not data or not isinstance(data, dict):
            print("ERROR: Invalid data structure")
            return jsonify({"error": "Invalid preferences data"}), 400
            
        # Ensure we only update allowed fields
        allowed_fields = ['health_goals', 'dietary_restrictions']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        print(f"Filtered update data: {update_data}")
        
        if not update_data:
            print("ERROR: No valid fields to update")
            return jsonify({"error": "No valid preferences to update"}), 400
            
        # Validate the types of the fields
        for field, value in update_data.items():
            print(f"\nChecking field: {field}")
            print(f"Value type: {type(value)}")
            print(f"Value: {value}")
            
            if not isinstance(value, list):
                print(f"ERROR: {field} is not a list")
                return jsonify({"error": f"{field} must be an array"}), 422
                
            if field == 'health_goals':
                for goal in value:
                    if not isinstance(goal, str):
                        print(f"ERROR: Invalid goal type: {type(goal)}")
                        return jsonify({"error": "health_goals must contain only strings"}), 422
                        
            if field == 'dietary_restrictions':
                for restriction in value:
                    if not isinstance(restriction, str):
                        print(f"ERROR: Invalid restriction type: {type(restriction)}")
                        return jsonify({"error": "dietary_restrictions must contain only strings"}), 422
            
        print("\nData validation passed, attempting update...")
        
        # Update user preferences
        success = User.update_preferences(user_id, update_data)
        
        if success:
            print("Update successful!")
            return jsonify({"message": "Preferences updated successfully"}), 200
        else:
            print("Update failed!")
            return jsonify({"error": "Failed to update preferences"}), 500
            
    except Exception as e:
        print(f"\nEXCEPTION OCCURRED: {str(e)}")
        return jsonify({"error": str(e)}), 500

@user_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Return only the preferences fields
        preferences = {
            "health_goals": user.get('health_goals', []),
            "dietary_restrictions": user.get('dietary_restrictions', [])
        }
        
        return jsonify(preferences), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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