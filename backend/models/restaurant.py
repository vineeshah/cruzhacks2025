from datetime import datetime
from bson import ObjectId
from run import mongo
from pymongo import MongoClient
from config import Config
from services.google_places_service import GooglePlacesService

db = mongo.db

class Restaurant:
    @staticmethod
    def find_by_id(place_id):
        """Find a restaurant by its Google Places ID"""
        try:
            restaurant = mongo.db.restaurants.find_one({"place_id": place_id})
            if restaurant:
                restaurant['id'] = str(restaurant.pop('_id'))
            return restaurant
        except:
            return None
    
    @staticmethod
    def create_or_update(place_data):
        """Create or update a restaurant"""
        try:
            result = mongo.db.restaurants.update_one(
                {"place_id": place_data['place_id']},
                {"$set": place_data},
                upsert=True
            )
            return result.upserted_id or place_data['place_id']
        except:
            return None

    @staticmethod
    def create_from_places(places_data: dict, menu_items: list = None):
        """Create restaurant from Google Places data"""
        restaurant = {
            "places_id": places_data.get("place_id"),
            "name": places_data.get("name"),
            "address": places_data.get("formatted_address"),
            "rating": places_data.get("rating", 0),
            "price_level": places_data.get("price_level", 0),
            "types": places_data.get("types", []),
            "website": places_data.get("website", ""),
            "opening_hours": places_data.get("opening_hours", {}),
            "location": {
                "coordinates": [
                    places_data["geometry"]["location"]["lng"],
                    places_data["geometry"]["location"]["lat"]
                ]
            },
            "menu_items": menu_items or [],
            "health_rating": 0,  # To be calculated
            "user_ratings": [],  # Store user-specific ratings
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Check if restaurant already exists
        existing = db.restaurants.find_one({"places_id": restaurant["places_id"]})
        if existing:
            # Update existing restaurant
            db.restaurants.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "name": restaurant["name"],
                    "address": restaurant["address"],
                    "rating": restaurant["rating"],
                    "price_level": restaurant["price_level"],
                    "types": restaurant["types"],
                    "website": restaurant["website"],
                    "opening_hours": restaurant["opening_hours"],
                    "location": restaurant["location"],
                    "updated_at": datetime.utcnow()
                }}
            )
            restaurant["_id"] = existing["_id"]
        else:
            # Insert new restaurant
            result = db.restaurants.insert_one(restaurant)
            restaurant["_id"] = result.inserted_id
            
        return restaurant
    
    @staticmethod
    def update_menu_items(restaurant_id: str, menu_items: list):
        """Update restaurant menu items and recalculate health rating"""
        db.restaurants.update_one(
            {"_id": ObjectId(restaurant_id)},
            {
                "$set": {
                    "menu_items": menu_items,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return Restaurant.find_by_id(restaurant_id)
    
    @staticmethod
    def add_user_rating(restaurant_id: str, user_id: str, rating: int, comment: str = None):
        """Add a user rating for the restaurant"""
        rating_data = {
            "user_id": user_id,
            "rating": rating,
            "comment": comment,
            "created_at": datetime.utcnow()
        }
        
        db.restaurants.update_one(
            {"_id": ObjectId(restaurant_id)},
            {
                "$push": {"user_ratings": rating_data},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return Restaurant.find_by_id(restaurant_id)
    
    @staticmethod
    def find_by_places_id(places_id: str):
        return db.restaurants.find_one({"places_id": places_id})
    
    @staticmethod
    def search_nearby(location: list, radius: int = 5000):
        """Find restaurants near a location"""
        return list(db.restaurants.find({
            "location.coordinates": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": location
                    },
                    "$maxDistance": radius
                }
            }
        }))

    @staticmethod
    def find_nearby(lat, lng, radius_km):
        """Find restaurants within radius_km of given coordinates"""
        # Convert km to meters for MongoDB
        radius_meters = radius_km * 1000
        
        return list(db.restaurants.find({
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lng, lat]
                    },
                    "$maxDistance": radius_meters
                }
            }
        }))

    @staticmethod
    def get_menu_health_rating(restaurant_id):
        """Get overall health rating for restaurant's menu"""
        restaurant = Restaurant.find_by_id(restaurant_id)
        if not restaurant:
            return None
            
        menu_items = restaurant.get('menu_items', [])
        if not menu_items:
            return 5  # Default rating if no menu items
            
        # Calculate average health rating
        total_rating = 0
        for item in menu_items:
            # Get health rating for each menu item
            health_rating = db.foods.find_one(
                {"name": item},
                {"health_rating": 1}
            )
            if health_rating:
                total_rating += health_rating.get('health_rating', 5)
            else:
                total_rating += 5  # Default rating
                
        return round(total_rating / len(menu_items), 1)

    @staticmethod
    def find_by_food(food_name, lat=None, lng=None, radius_km=5):
        """Find restaurants serving specific food"""
        query = {
            "menu_items": {
                "$regex": food_name,
                "$options": "i"  # Case insensitive
            }
        }
        
        # Add location filter if coordinates provided
        if lat and lng:
            radius_meters = radius_km * 1000
            query["location"] = {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lng, lat]
                    },
                    "$maxDistance": radius_meters
                }
            }
            
        return list(db.restaurants.find(query))

    @staticmethod
    def fetch_menu_items(restaurant_id):
        """Fetch menu items from Google Places API"""
        restaurant = Restaurant.find_by_id(restaurant_id)
        if not restaurant:
            return None
        
        # Use Google Places API to get menu
        menu_items = GooglePlacesService.get_menu(restaurant['places_id'])
        
        # Update database
        Restaurant.update_menu_items(restaurant_id, menu_items)
        return menu_items