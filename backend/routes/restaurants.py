from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.google_places_service import GooglePlacesService
from services.recs import RecommendationService
from models.user import User
from models.restaurant import Restaurant

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/api/restaurants')
google_places_service = GooglePlacesService()
rec_service = RecommendationService()

@restaurants_bp.route('/search', methods=['GET'])
@jwt_required()
def search_restaurants():
    print("Searching for restaurants")
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        print(f"Search request from user: {user_id}")

        # Get query parameters
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', type=int)

        if not all([lat, lng, radius]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Get user preferences
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_preferences = {
            "health_goals": user.get('health_goals', []),
            "dietary_restrictions": user.get('dietary_restrictions', [])
        }

        # Search for restaurants
        location = f"{lat},{lng}"
        places = google_places_service.search_places(
            location=location,
            radius=radius,
            user_preferences=user_preferences
        )

        return jsonify(places)

    except Exception as e:
        print(f"Error in search_restaurants: {str(e)}")
        return jsonify({'error': str(e)}), 500

@restaurants_bp.route('/<place_id>', methods=['GET'])
@jwt_required()
def get_restaurant_details(place_id):
    try:
        # Get current user from JWT token
        current_user = get_jwt_identity()
        print(f"Getting details for restaurant {place_id} for user: {current_user}")
        
        # Get place details from Google Places API
        place_details = google_places_service.get_place_details(place_id)
        
        if not place_details:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        # Get user preferences
        user = User.find_by_id(current_user)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Add user preferences to the response
        place_details['user_preferences'] = {
            'health_goals': user.get('health_goals', []),
            'dietary_restrictions': user.get('dietary_restrictions', [])
        }
        
        return jsonify(place_details)
        
    except Exception as e:
        print(f"Error in get_restaurant_details: {str(e)}")
        return jsonify({'error': str(e)}), 500

