from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.recipe_search import RecipeSearchService

food_bp = Blueprint('food', __name__, url_prefix='/api/food')
rec_service = RecipeSearchService()

@food_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_food():
    try:
        data = request.get_json()
        food_name = data.get('food_name')
        
        if not food_name:
            return jsonify({"error": "Food name is required"}), 400
        
        analysis = rec_service.analyze_food_health(food_name)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/alternatives', methods=['POST'])
@jwt_required()
def get_food_alternatives():
    try:
        data = request.get_json()
        food_name = data.get('food_name')
        user_id = get_jwt_identity()
        
        if not food_name:
            return jsonify({"error": "Food name is required"}), 400
        
        alternatives = rec_service.get_healthier_food_alternatives(food_name, user_id)
        return jsonify(alternatives), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/recipe-alternatives', methods=['POST'])
@jwt_required()
def get_recipe_alternatives():
    try:
        data = request.get_json()
        food_item = data.get('food_item')
        user_id = get_jwt_identity()
        
        if not food_item:
            return jsonify({"error": "Food item is required"}), 400
        
        alternatives = rec_service.get_recipe_recommendations(food_item, user_id)
        return jsonify(alternatives)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

