import google.generativeai as genai
from models import Restaurant, Food
from config import Config
import requests
from typing import List, Dict
import os

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class RestaurantService:
    @staticmethod
    def get_nearby_restaurants(location: List[float], radius: int = 5000) -> List[Dict]:
        """Get nearby restaurants using Google Places API"""
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            'location': f"{location[0]},{location[1]}",
            'radius': radius,
            'type': 'restaurant',
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        restaurants = []
        for place in data.get('results', []):
            # Get detailed place information
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place['place_id'],
                'fields': 'name,formatted_address,rating,price_level,types,website,opening_hours',
                'key': api_key
            }
            
            details_response = requests.get(details_url, params=details_params)
            details = details_response.json().get('result', {})
            
            restaurant = {
                'name': place['name'],
                'address': details.get('formatted_address', ''),
                'rating': place.get('rating', 0),
                'price_level': details.get('price_level', 0),
                'types': place.get('types', []),
                'website': details.get('website', ''),
                'opening_hours': details.get('opening_hours', {}),
                'location': {
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng']
                }
            }
            restaurants.append(restaurant)
        
        return restaurants

    @staticmethod
    def analyze_menu_health(menu_items: List[str]) -> float:
        """Analyze menu items using Gemini to determine health rating"""
        prompt = f"""
        Analyze these menu items and rate their overall healthiness on a scale of 1-10:
        {', '.join(menu_items)}
        
        Consider:
        - Nutritional content
        - Processing level
        - Freshness of ingredients
        - Cooking methods
        
        Return only the number rating.
        """
        
        response = model.generate_content(prompt)
        try:
            rating = float(response.text.strip())
            return min(max(rating, 1), 10)  # Ensure rating is between 1-10
        except:
            return 5.0  # Default rating if analysis fails

    @staticmethod
    def get_healthier_options(restaurant_id: str, user_preferences: Dict) -> List[Dict]:
        """Get healthier menu options based on user preferences"""
        restaurant = Restaurant.find_by_id(restaurant_id)
        if not restaurant:
            return []
        
        prompt = f"""
        User preferences:
        - Health goals: {user_preferences.get('health_goals', [])}
        - Dietary restrictions: {user_preferences.get('dietary_restrictions', [])}
        - Budget: {user_preferences.get('budget_preference', 'medium')}
        
        Restaurant menu items:
        {restaurant.get('menu_items', [])}
        
        Suggest 3 healthier options from the menu that align with the user's preferences.
        For each option, provide:
        1. Item name
        2. Brief explanation of why it's a good choice
        3. Estimated health rating (1-10)
        
        Format the response as a JSON array of objects with 'name', 'explanation', and 'rating' fields.
        """
        
        response = model.generate_content(prompt)
        try:
            # Parse the response into structured data
            suggestions = eval(response.text)  # Note: In production, use proper JSON parsing
            return suggestions
        except:
            return [] 