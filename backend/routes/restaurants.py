from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.restaurant_service import RestaurantService
from services.recs import RecommendationService
from models import User
from models.restaurant import Restaurant
from bson import ObjectId
from services.google_places_service import GooglePlacesService

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/api/restaurants')
places_service = GooglePlacesService()
rec_service = RecommendationService()

@restaurant_bp.route('/nearby', methods=['GET'])
@jwt_required()
def get_nearby_restaurants():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 5))  # Default 5km radius
        
        restaurants = Restaurant.find_nearby(lat, lng, radius)
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@restaurant_bp.route('/search', methods=['GET'])
@jwt_required()
def search_restaurants():
    try:
        location = request.args.get('location')
        radius = int(request.args.get('radius', 5000))  # Default 5km radius
        keyword = request.args.get('keyword', 'restaurant')
        
        if not location:
            return jsonify({"error": "Location is required"}), 400
        
        results = places_service.search_places(location, radius, keyword)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<place_id>', methods=['GET'])
@jwt_required()
def get_restaurant(place_id):
    try:
        restaurant = places_service.get_place_details(place_id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        
        # Save to database
        Restaurant.create_or_update(restaurant)
        
        return jsonify(restaurant)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<restaurant_id>/recommendations', methods=['GET'])
@jwt_required()
def get_restaurant_recommendations(restaurant_id):
    try:
        user_id = get_jwt_identity()
        recommendations = rec_service.get_restaurant_recommendations(restaurant_id, user_id)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<restaurant_id>/healthier-options', methods=['GET'])
@jwt_required()
def get_healthier_options(restaurant_id):
    try:
        user_id = get_jwt_identity()
        options = rec_service.get_healthier_options(restaurant_id, user_id)
        return jsonify(options)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<restaurant_id>/menu-health', methods=['GET'])
@jwt_required()
def get_menu_health(restaurant_id):
    try:
        health_rating = Restaurant.get_menu_health_rating(restaurant_id)
        return jsonify({"health_rating": health_rating}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@restaurant_bp.route('/search-by-food', methods=['GET'])
@jwt_required()
def search_restaurants_by_food():
    try:
        food_name = request.args.get('food')
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 5))  # Default 5km radius
        user_id = get_jwt_identity()
        
        # Get nearby restaurants
        restaurants = Restaurant.find_nearby(lat, lng, radius)
        
        # Filter restaurants that serve the food
        matching_restaurants = []
        for restaurant in restaurants:
            menu_items = restaurant.get('menu_items', [])
            if any(food_name.lower() in item.lower() for item in menu_items):
                # Get health rating for the specific food
                food_health = RecommendationService().analyze_food_health(food_name)
                
                matching_restaurants.append({
                    "restaurant_id": str(restaurant['_id']),
                    "name": restaurant['name'],
                    "address": restaurant['address'],
                    "distance": restaurant['distance'],
                    "food_item": food_name,
                    "health_rating": food_health['rating'],
                    "price": restaurant.get('price_range', 'N/A')
                })
        
        # Sort by health rating and distance
        matching_restaurants.sort(key=lambda x: (-x['health_rating'], x['distance']))
        
        return jsonify(matching_restaurants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
