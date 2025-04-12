from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.google_places_service import GooglePlacesService
from services.recs import RecommendationService
from models.user import User
from models.restaurant import Restaurant

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/api/restaurants')
places_service = GooglePlacesService()
rec_service = RecommendationService()

@restaurant_bp.route('/search', methods=['GET'])
@jwt_required()
def search_restaurants():
    """Search for nearby restaurants and get recommendations"""
    try:
        # Get search parameters
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 5))  # Default 5km radius
        user_id = get_jwt_identity()
        
        # Get user preferences
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        user_preferences = {
            "health_goals": user.get('health_goals', []),
            "dietary_restrictions": user.get('dietary_restrictions', [])
        }
        
        # Search for nearby restaurants
        location = f"{lat},{lng}"
        places = places_service.search_places(
            location=location,
            radius=radius * 1000,  # Convert km to meters
            user_preferences=user_preferences
        )
        
        # Store and format results with recommendations
        results = []
        for place in places:
            # Get detailed place information
            details = places_service.get_place_details(place['place_id'])
            if details:
                # Store in database
                restaurant_id = Restaurant.create_or_update(details)
                if restaurant_id:
                    # Get health analysis for the restaurant
                    health_analysis = rec_service.get_menu_health(restaurant_id, user_id)
                    if health_analysis and 'error' not in health_analysis:
                        details['health_analysis'] = health_analysis
                    results.append(details)
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<place_id>', methods=['GET'])
@jwt_required()
def get_restaurant(place_id):
    """Get detailed information about a specific restaurant"""
    try:
        # First check if we have it in our database
        restaurant = Restaurant.find_by_id(place_id)
        
        if not restaurant:
            # If not in database, fetch from Google Places
            details = places_service.get_place_details(place_id)
            
            if not details:
                return jsonify({"error": "Restaurant not found"}), 404
            
            # Store in database
            restaurant_id = Restaurant.create_or_update(details)
            if not restaurant_id:
                return jsonify({"error": "Failed to store restaurant data"}), 500
            
            restaurant = details
        
        # Get health analysis for the restaurant
        user_id = get_jwt_identity()
        health_analysis = rec_service.get_menu_health(place_id, user_id)
        if health_analysis and 'error' not in health_analysis:
            restaurant['health_analysis'] = health_analysis
        
        return jsonify(restaurant)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

