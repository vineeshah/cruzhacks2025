from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.food import Food
from services.food_service import FoodService
from services.recs import RecommendationService

food_bp = Blueprint('food', __name__, url_prefix='/api/food')
rec_service = RecommendationService()

@food_bp.route('/', methods=['POST'])
@jwt_required()
def create_food():
    try:
        data = request.get_json()
        food = Food.create(
            name=data['name'],
            category=data['category'],
            nutrition_info=data['nutrition_info'],
            ingredients=data.get('ingredients'),
            processing_level=data.get('processing_level')
        )
        return jsonify(food), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@food_bp.route('/<food_id>', methods=['GET'])
@jwt_required()
def get_food(food_id):
    try:
        food = Food.find_by_id(food_id)
        if not food:
            return jsonify({"error": "Food not found"}), 404
        return jsonify(food), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@food_bp.route('/search', methods=['GET'])
@jwt_required()
def search_food():
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))
        foods = Food.search(query, limit)
        return jsonify(foods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@food_bp.route('/<food_id>/alternatives', methods=['GET'])
@jwt_required()
def get_food_alternatives(food_id):
    try:
        user_id = get_jwt_identity()
        alternatives = rec_service.get_healthier_food_alternatives(food_id, user_id)
        return jsonify(alternatives), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@food_bp.route('/<food_id>/recipes', methods=['GET'])
@jwt_required()
def get_recipe_recommendations(food_id):
    try:
        user_id = get_jwt_identity()
        recipes = rec_service.get_recipe_recommendations(food_id, user_id)
        return jsonify(recipes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

