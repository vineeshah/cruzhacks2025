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
        """Search for places near a location"""
        try:
            # Create search criteria based on user preferences
            search_criteria = {
                'location': location,
                'radius': radius,
                'type': 'restaurant'
            }
            
            if user_preferences:
                # Add dietary restrictions to search
                if 'dietary_restrictions' in user_preferences:
                    restrictions = user_preferences['dietary_restrictions']
                    if 'vegetarian' in restrictions:
                        search_criteria['keyword'] = 'vegetarian restaurant'
                    elif 'vegan' in restrictions:
                        search_criteria['keyword'] = 'vegan restaurant'
                    elif 'gluten-free' in restrictions:
                        search_criteria['keyword'] = 'gluten free restaurant'
                
                # Add health-focused keywords
                if 'health_goals' in user_preferences:
                    goals = user_preferences['health_goals']
                    if 'weight_loss' in goals:
                        search_criteria['keyword'] = 'healthy restaurant'
                    elif 'muscle_gain' in goals:
                        search_criteria['keyword'] = 'protein restaurant'
            
            # Perform the search
            places = self.client.places_nearby(**search_criteria)
            
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
            
            return results
        except Exception as e:
            print(f"Error searching places: {str(e)}")
            return []

    def get_place_details(self, place_id):
        """Get detailed information about a place"""
        try:
            # Get basic place details
            details = self.client.place(place_id, fields=['name', 'formatted_address', 'geometry', 'rating', 'price_level', 'types', 'website', 'opening_hours'])
            
            if not details or 'result' not in details:
                return None
            
            place = details['result']
            
            # Get menu data if available
            menu_items = []
            if 'website' in place:
                try:
                    menu_data = self.client.place(place_id, fields=['menu'])
                    if menu_data and 'result' in menu_data and 'menu' in menu_data['result']:
                        menu = menu_data['result']['menu']
                        if 'items' in menu:
                            menu_items = [{
                                'name': item.get('name', ''),
                                'description': item.get('description', ''),
                                'price': item.get('price', '')
                            } for item in menu['items']]
                except:
                    pass  # Menu data not available
            
            return {
                "place_id": place_id,
                "name": place.get('name'),
                "address": place.get('formatted_address'),
                "location": place.get('geometry', {}).get('location'),
                "rating": place.get('rating'),
                "price_level": place.get('price_level'),
                "types": place.get('types', []),
                "website": place.get('website'),
                "opening_hours": place.get('opening_hours', {}).get('weekday_text', []),
                "menu_items": menu_items
            }
        except Exception as e:
            print(f"Error getting place details: {str(e)}")
            return None

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