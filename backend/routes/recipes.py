from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.recs import RecommendationService
from models.user import User


recipe_bp = Blueprint('recipe', __name__, url_prefix='/api/recipes')
rec_service = RecommendationService()

@recipe_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_recipe():
    try:
        data = request.get_json()
        recipe_name = data.get('recipe_name')
        ingredients = data.get('ingredients', [])
        
        if not recipe_name:
            return jsonify({"error": "Recipe name is required"}), 400
        
        analysis = rec_service.analyze_recipe_health(recipe_name, ingredients)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recipe_bp.route('/alternatives', methods=['POST'])
@jwt_required()
def get_recipe_alternatives():
    try:
        data = request.get_json()
        recipe_name = data.get('recipe_name')
        ingredients = data.get('ingredients', [])
        user_id = get_jwt_identity()
        
        if not recipe_name:
            return jsonify({"error": "Recipe name is required"}), 400
        
        alternatives = rec_service.get_recipe_recommendations(recipe_name, ingredients, user_id)
        return jsonify(alternatives)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


