import os
from googlemaps import Client
from config import Config

class GooglePlacesService:
    def __init__(self):
        self.client = Client(key=Config.GOOGLE_PLACES_API_KEY)

    def get_menu(self, place_id):
        """Get menu items for a place"""
        try:
            # Get place details
            place_details = self.client.place(place_id, fields=['types', 'name', 'menu_items'])
            if not place_details:
                return []
            
            # Check if it's a food establishment
            if 'types' not in place_details or not any(t in place_details['types'] for t in ['restaurant', 'food', 'cafe', 'bar']):
                return []
            
            # Get menu items
            menu_items = place_details.get('menu_items', [])
            
            # Format menu items
            formatted_items = []
            for item in menu_items:
                formatted_items.append({
                    'name': item.get('name', ''),
                    'description': item.get('description', ''),
                    'price': item.get('price', ''),
                    'category': item.get('category', '')
                })
            
            return formatted_items
        except Exception as e:
            print(f"Error getting menu: {str(e)}")
            return []

    def search_places(self, location, radius, user_preferences=None):
        """Search for places near a location with optional user preferences filtering"""
        try:
            print(f"\nSearching places with location: {location}, radius: {radius}")
            print(f"User preferences: {user_preferences}")
            
            # Convert location to tuple if it's a string
            if isinstance(location, str):
                lat, lng = map(float, location.split(','))
                location = (lat, lng)
            
            # Convert radius to meters if it's in miles
            if radius > 100:  # Assuming radius > 100 means it's in miles
                radius = int(radius * 1609.34)  # Convert miles to meters
            
            # Create search criteria
            search_criteria = {
                'location': location,
                'radius': radius,
                'type': 'restaurant',
                'language': 'en'
            }
            
            # Add keyword based on user preferences
            if user_preferences:
                if 'health_goals' in user_preferences:
                    health_goals = user_preferences['health_goals']
                    if 'Vegetarian' in health_goals:
                        search_criteria['keyword'] = 'vegetarian'
                    elif 'Vegan' in health_goals:
                        search_criteria['keyword'] = 'vegan'
                    elif 'Gluten-Free' in health_goals:
                        search_criteria['keyword'] = 'gluten free'
                    elif 'Low Carb' in health_goals:
                        search_criteria['keyword'] = 'low carb'
            
            print(f"Search criteria: {search_criteria}")
            
            # Perform the search
            places = self.client.places_nearby(**search_criteria)
            print(f"Places response: {places}")
            
            # Format results
            results = []
            for place in places.get('results', []):
                result = {
                    'place_id': place['place_id'],
                    'name': place['name'],
                    'address': place.get('vicinity', ''),
                    'rating': place.get('rating', 0),
                    'price_level': place.get('price_level', 0),
                    'types': place.get('types', [])
                }
                results.append(result)
            
            print(f"Found {len(results)} places")
            return results
            
        except Exception as e:
            print(f"\nError in search_places: {str(e)}")
            print(f"Error type: {type(e)}")
            return []

    def get_place_details(self, place_id):
        """Get detailed information about a place"""
        try:
            place = self.client.place(
                place_id,
                fields=['name', 'formatted_address', 'rating', 'price_level', 'website', 'opening_hours']
            )
            return place.get('result', {})
        except Exception as e:
            print(f"Error getting place details: {str(e)}")
            return {}

    # def search_places(self, location, radius, keyword='restaurant'):
    #     """Search for places with menu data"""
    #     try:
    #         results = self.client.places_nearby(
    #             location=location,
    #             radius=radius,
    #             keyword=keyword,
    #             type='restaurant'
    #         )
            
    #         places = []
    #         for place in results.get('results', []):
    #             # Get basic details
    #             place_details = {
    #                 'place_id': place['place_id'],
    #                 'name': place['name'],
    #                 'rating': place.get('rating', 0),
    #                 'price_level': place.get('price_level', 0),
    #                 'types': place.get('types', []),
    #                 'geometry': place.get('geometry', {}),
    #                 'vicinity': place.get('vicinity', '')
    #             }
                
    #             # Check if menu is available
    #             if 'menu' in place.get('types', []):
    #                 place_details['has_menu'] = True
                
    #             places.append(place_details)
            
    #         return places
    #     except Exception as e:
    #         print(f"Error searching places: {e}")
    #         return [] 