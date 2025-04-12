from datetime import datetime
from bson import ObjectId
from run import mongo

class Food:
    @staticmethod
    def create(name, category, nutrition_info, ingredients=None, processing_level=None):
        food = {
            "name": name,
            "category": category,  # e.g., "fast_food", "home_cooked", "restaurant", "packaged"
            "nutrition_info": nutrition_info,  # Dict with calories, protein, fat, etc.
            "ingredients": ingredients or [],
            "processing_level": processing_level or "medium",  # "low", "medium", "high"
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = mongo.db.foods.insert_one(food)
        food["_id"] = result.inserted_id
        return food
    
    @staticmethod
    def find_by_id(food_id):
        return mongo.db.foods.find_one({"_id": ObjectId(food_id)})
    
    @staticmethod
    def find_by_name(name):
        return mongo.db.foods.find_one({"name": {"$regex": name, "$options": "i"}})
    
    @staticmethod
    def search(query, limit=10):
        return list(mongo.db.foods.find(
            {"name": {"$regex": query, "$options": "i"}}
        ).limit(limit))