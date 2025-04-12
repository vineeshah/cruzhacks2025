import googlemaps
from config import Config

class GooglePlacesService:
    def __init__(self):
        self.client = googlemaps.Client(key=Config.GOOGLE_PLACES_API_KEY)

    def get_menu(self, place_id):
        """Get menu items for a place"""
        try:
            place_details = self.client.place(place_id, fields=['menu'])
            return place_details.get('menu', [])
        except Exception as e:
            print(f"Error fetching menu: {e}")
            return [] 