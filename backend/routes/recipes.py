from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.recipe import Recipe
from services.recs import RecommendationService

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    try:
        data = request.get_json()
        recipe = Recipe.create(
            name=data['name'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            nutrition_info=data['nutrition_info'],
            difficulty=data['difficulty'],
            prep_time=data['prep_time'],
            cook_time=data['cook_time'],
            tags=data.get('tags')
        )
        return jsonify(recipe), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@recipe_bp.route('/<recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe(recipe_id):
    try:
        recipe = Recipe.find_by_id(recipe_id)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404
        return jsonify(recipe), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@recipe_bp.route('/search', methods=['GET'])
@jwt_required()
def search_recipes():
    try:
        query = request.args.get('q')
        tags = request.args.getlist('tags')
        limit = int(request.args.get('limit', 10))
        recipes = Recipe.search(query, tags, limit)
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@recipe_bp.route('/<recipe_id>/recommendations', methods=['GET'])
@jwt_required()
def get_recipe_recommendations(recipe_id):
    try:
        user_id = get_jwt_identity()
        recommendations = RecommendationService().get_recipe_recommendations(recipe_id, user_id)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
