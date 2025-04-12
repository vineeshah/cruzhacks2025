from datetime import datetime
from bson import ObjectId
from run import mongo

class Recipe:
    @staticmethod
    def create(name, ingredients, instructions, nutrition_info, difficulty, prep_time, cook_time, tags=None):
        recipe = {
            "name": name,
            "ingredients": ingredients,  # List of dicts with ingredient name, amount, unit
            "instructions": instructions,  # List of steps
            "nutrition_info": nutrition_info,
            "difficulty": difficulty,  # "easy", "medium", "hard"
            "prep_time": prep_time,  # In minutes
            "cook_time": cook_time,  # In minutes
            "tags": tags or [],  # e.g., ["healthy", "quick", "vegetarian"]
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = mongo.db.recipes.insert_one(recipe)
        recipe["_id"] = result.inserted_id
        return recipe
    
    @staticmethod
    def find_by_id(recipe_id):
        return mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    @staticmethod
    def search(query, tags=None, limit=10):
        search_query = {"name": {"$regex": query, "$options": "i"}}
        if tags:
            search_query["tags"] = {"$in": tags}
        return list(mongo.db.recipes.find(search_query).limit(limit))