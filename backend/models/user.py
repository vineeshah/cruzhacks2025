from run import mongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create(email, password, name=None):
        """Create a new user"""
        if User.find_by_email(email):
            return None
        
        # Default health goals
        default_health_goals = [
            "Balanced Diet",
            "Weight Management",
            "Energy Boost"
        ]

        # Default dietary restrictions (empty list)
        default_dietary_restrictions = []
        
        user_data = {
            "email": email,
            "password": generate_password_hash(password),
            "name": name,
            "health_goals": default_health_goals,
            "dietary_restrictions": default_dietary_restrictions
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
            print(f"Updating preferences for user {user_id}")
            print(f"Preferences data: {preferences}")
            
            # Convert string ID to ObjectId
            user_id = ObjectId(user_id)
            
            # Prepare the update data
            update_data = {}
            if 'health_goals' in preferences:
                update_data['health_goals'] = preferences['health_goals']
            if 'dietary_restrictions' in preferences:
                update_data['dietary_restrictions'] = preferences['dietary_restrictions']
            
            print(f"Final update data: {update_data}")
            
            # Perform the update
            result = mongo.db.users.update_one(
                {"_id": user_id},
                {"$set": update_data}
            )
            
            print(f"Update result: {result.modified_count} documents modified")
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating preferences: {str(e)}")
            return False
