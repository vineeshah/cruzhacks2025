from bson import ObjectId
from db import mongo
from datetime import datetime

class User:
    @staticmethod
    def create(username, email, password_hash=None, health_goals=None, dietary_restrictions=None, budget_preference=None, google_id=None):
        user = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "google_id": google_id,
            "health_goals": health_goals or [],  # e.g., ["weight_loss", "low_sodium"]
            "dietary_restrictions": dietary_restrictions or [],  # e.g., ["vegetarian", "gluten_free"]
            "budget_preference": budget_preference or "medium",  # "low", "medium", "high"
            "favorite_foods": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = mongo.db.users.insert_one(user)
        user["_id"] = result.inserted_id
        return user
    
    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})
    
    @staticmethod
    def find_by_google_id(google_id):
        return mongo.db.users.find_one({"google_id": google_id})
    
    @staticmethod
    def update(user_id, update_data):
        update_data["updated_at"] = datetime.utcnow()
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return User.find_by_id(user_id)
    
    @staticmethod
    def add_favorite_food(user_id, food_item):
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorite_foods": food_item}}
        )
        return User.find_by_id(user_id)
