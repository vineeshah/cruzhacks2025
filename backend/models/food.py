from run import mongo
from bson import ObjectId

class Food:
    @staticmethod
    def find_by_id(food_id):
        """Find a food item by ID"""
        try:
            food = mongo.db.food_items.find_one({"_id": ObjectId(food_id)})
            if food:
                food['id'] = str(food.pop('_id'))
            return food
        except:
            return None
    
    @staticmethod
    def create(food_data):
        """Create a new food item"""
        try:
            result = mongo.db.food_items.insert_one(food_data)
            return str(result.inserted_id)
        except:
            return None