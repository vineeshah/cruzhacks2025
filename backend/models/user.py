from run import mongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create(email, password, name=None):
        """Create a new user"""
        if User.find_by_email(email):
            return None
        
        user_data = {
            "email": email,
            "password": generate_password_hash(password),
            "name": name,
            "health_goals": [],
            "dietary_restrictions": []
        }
        
        result = mongo.db.users.insert_one(user_data)
        return User.find_by_id(str(result.inserted_id))
    
    @staticmethod
    def find_by_id(user_id):
        """Find a user by ID"""
        try:
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user['id'] = str(user.pop('_id'))
            return user
        except:
            return None
    
    @staticmethod
    def find_by_email(email):
        """Find a user by email"""
        user = mongo.db.users.find_one({"email": email})
        if user:
            user['id'] = str(user.pop('_id'))
        return user
    
    @staticmethod
    def verify_password(user, password):
        """Verify user password"""
        return check_password_hash(user['password'], password)
    
    @staticmethod
    def update_preferences(user_id, preferences):
        """Update user preferences"""
        try:
            result = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": preferences}
            )
            return result.modified_count > 0
        except:
            return False
