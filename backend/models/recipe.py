from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.recipe_search import RecipeSearchService
from models.user import User
from run import mongo
from bson import ObjectId
from datetime import datetime


recipe_bp = Blueprint('recipe', __name__, url_prefix='/api/recipes')
rec_service = RecipeSearchService()

@recipe_bp.route('/recommend', methods=['GET'])
@jwt_required()
def recommend_recipes():
    '''Finds user preferences, calls recipe_search service to search for recipes based on user's preferences'''
    try:
        user_id = get_jwt_identity()
        
        # Get user preferences
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user_preferences = []
        health_goals = user.get('health_goals', [])
        dietary_restrictions = user.get('dietary_restrictions', [])

        if health_goals is not []:
            for goal in health_goals:
                user_preferences.append(goal)

        if dietary_restrictions is not []:
            for entry in dietary_restrictions:
                user_preferences.append(entry)

        recommendations = rec_service.search_recipes(user_preferences)
        return jsonify(recommendations), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


'''
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

'''

class Recipe:
    @staticmethod
    def find_by_id(recipe_id):
        """Find a recipe by ID"""
        try:
            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
            if recipe:
                recipe['id'] = str(recipe.pop('_id'))
            return recipe
        except:
            return None

    @staticmethod
    def create(recipe_data):
        """Create a new recipe"""
        try:
            recipe_data.update({
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            result = mongo.db.recipes.insert_one(recipe_data)
            return str(result.inserted_id)
        except:
            return None

    @staticmethod
    def update(recipe_id, recipe_data):
        """Update an existing recipe"""
        try:
            recipe_data["updated_at"] = datetime.utcnow()
            mongo.db.recipes.update_one(
                {"_id": ObjectId(recipe_id)},
                {"$set": recipe_data}
            )
            return True
        except:
            return False

    @staticmethod
    def delete(recipe_id):
        """Delete a recipe"""
        try:
            mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
            return True
        except:
            return False

    @staticmethod
    def search_by_preferences(preferences):
        """Search recipes by user preferences"""
        try:
            query = {
                "$or": [
                    {"health_goals": {"$in": preferences}},
                    {"dietary_restrictions": {"$in": preferences}}
                ]
            }
            recipes = list(mongo.db.recipes.find(query))
            for recipe in recipes:
                recipe['id'] = str(recipe.pop('_id'))
            return recipes
        except:
            return []

    @staticmethod
    def add_rating(recipe_id, user_id, rating, comment=None):
        """Add a user rating to a recipe"""
        try:
            rating_data = {
                "user_id": user_id,
                "rating": rating,
                "comment": comment,
                "created_at": datetime.utcnow()
            }
            
            mongo.db.recipes.update_one(
                {"_id": ObjectId(recipe_id)},
                {
                    "$push": {"ratings": rating_data},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return True
        except:
            return False

    @staticmethod
    def get_average_rating(recipe_id):
        """Calculate average rating for a recipe"""
        try:
            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
            if not recipe or not recipe.get('ratings'):
                return 0
                
            ratings = [r['rating'] for r in recipe['ratings']]
            return sum(ratings) / len(ratings)
        except:
            return 0